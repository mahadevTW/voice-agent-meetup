const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const downloadBtn = document.getElementById("download-btn");
const statusEl = document.getElementById("status");
const audioEl = document.getElementById("agent-audio");
const transcriptLogEl = document.getElementById("transcript-log");
const transcriptEmptyEl = document.getElementById("transcript-empty");
const activityEl = document.getElementById("activity");
const activityTextEl = document.getElementById("activity-text");
const orbEl = document.getElementById("orb");
const waveformEl = document.getElementById("waveform");
const waveformBars = [...waveformEl.querySelectorAll("span")];

let pc = null;
let micStream = null;
let dataChannel = null;
let transcript = [];
const activeCalls = new Map();

let audioCtx = null;
let micAnalyser = null;
let remoteAnalyser = null;
let meterFrame = null;

const TOOL_LABELS = {
  get_weather: "Checking the weather",
  calculate: "Doing the math",
  get_order_status: "Checking order status",
};

function toolLabel(name) {
  return TOOL_LABELS[name] || `Running ${name.replace(/_/g, " ")}`;
}

function renderActivity() {
  orbEl.classList.toggle("is-thinking", activeCalls.size > 0);

  if (activeCalls.size === 0) {
    activityEl.hidden = true;
    return;
  }

  const labels = [...activeCalls.values()];
  activityTextEl.textContent =
    labels.length === 1 ? `${labels[0]}…` : `Running ${labels.length} tasks…`;
  activityEl.hidden = false;
}

function setOrbState(state) {
  orbEl.dataset.state = state;
}

startBtn.addEventListener("click", startSession);
stopBtn.addEventListener("click", stopSession);
downloadBtn.addEventListener("click", downloadTranscript);

async function startSession() {
  startBtn.disabled = true;
  setOrbState("connecting");
  statusEl.textContent = "Requesting session...";

  const sessionRes = await fetch("/realtime/session", { method: "POST" });
  const session = await sessionRes.json();
  const ephemeralKey = session.value;

  pc = new RTCPeerConnection();

  pc.ontrack = (event) => {
    audioEl.srcObject = event.streams[0];
    setupAnalyser(event.streams[0], "remote");
  };

  micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  pc.addTrack(micStream.getTracks()[0]);
  setupAnalyser(micStream, "mic");

  dataChannel = pc.createDataChannel("oai-events");
  dataChannel.addEventListener("message", (event) => {
    handleRealtimeEvent(JSON.parse(event.data));
  });

  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  statusEl.textContent = "Connecting to OpenAI...";

  const sdpResponse = await fetch("https://api.openai.com/v1/realtime/calls", {
    method: "POST",
    body: offer.sdp,
    headers: {
      Authorization: `Bearer ${ephemeralKey}`,
      "Content-Type": "application/sdp",
    },
  });

  await pc.setRemoteDescription({
    type: "answer",
    sdp: await sdpResponse.text(),
  });

  statusEl.textContent = "Connected — start talking";
  setOrbState("active");
  waveformEl.dataset.active = "true";
  stopBtn.hidden = false;
}

function stopSession() {
  micStream?.getTracks().forEach((track) => track.stop());
  pc?.close();
  micStream = null;
  pc = null;
  dataChannel = null;

  stopMeter();

  audioEl.srcObject = null;
  stopBtn.hidden = true;
  startBtn.disabled = false;
  statusEl.textContent = "Idle";
  setOrbState("idle");
  orbEl.classList.remove("is-speaking", "is-thinking");
  waveformEl.dataset.active = "false";

  activeCalls.clear();
  renderActivity();
}

// ---------- Live amplitude meter ----------
// Drives the orb glow and waveform bars from actual mic/agent audio levels,
// purely for visual feedback — playback routing is untouched.

function setupAnalyser(stream, kind) {
  audioCtx ||= new (window.AudioContext || window.webkitAudioContext)();

  const source = audioCtx.createMediaStreamSource(stream);
  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 64;
  source.connect(analyser);

  if (kind === "mic") {
    micAnalyser = analyser;
  } else {
    remoteAnalyser = analyser;
  }

  if (!meterFrame) {
    meterFrame = requestAnimationFrame(tickMeter);
  }
}

function levelFor(analyser) {
  if (!analyser) return 0;
  const data = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(data);
  const avg = data.reduce((sum, v) => sum + v, 0) / data.length;
  return Math.min(1, avg / 130);
}

function tickMeter() {
  const micLevel = levelFor(micAnalyser);
  const remoteLevel = levelFor(remoteAnalyser);
  const amp = Math.max(micLevel, remoteLevel);

  orbEl.style.setProperty("--amp", amp.toFixed(3));
  orbEl.classList.toggle("is-speaking", remoteLevel > 0.08 && remoteLevel >= micLevel);

  if (waveformEl.dataset.active === "true") {
    waveformBars.forEach((bar, i) => {
      const jitter = 0.55 + 0.45 * Math.sin(i * 1.7);
      bar.style.setProperty("--h", Math.max(0.12, amp * jitter).toFixed(3));
    });
  }

  meterFrame = requestAnimationFrame(tickMeter);
}

function stopMeter() {
  if (meterFrame) cancelAnimationFrame(meterFrame);
  meterFrame = null;
  micAnalyser = null;
  remoteAnalyser = null;
  orbEl.style.setProperty("--amp", 0);
}

function handleRealtimeEvent(event) {
  console.log("realtime event:", event);

  if (event.type === "conversation.item.input_audio_transcription.completed") {
    addTranscriptEntry("user", event.transcript);
  } else if (event.type === "response.output_audio_transcript.done") {
    addTranscriptEntry("agent", event.transcript);
  } else if (event.type === "response.done") {
    const functionCalls = (event.response.output || []).filter((item) => item.type === "function_call");
    functionCalls.forEach(runToolCall);
  }
}

async function runToolCall(call) {
  const args = JSON.parse(call.arguments);
  console.log("[tool call] request:", { name: call.name, arguments: args });

  activeCalls.set(call.call_id, toolLabel(call.name));
  renderActivity();

  let result;
  try {
    const res = await fetch("/tools/call", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: call.name, arguments: args }),
    });
    result = await res.json();
    console.log("[tool call] response:", result);
  } catch (err) {
    console.error("[tool call] failed:", err);
    result = { error: "Tool call failed" };
  } finally {
    activeCalls.delete(call.call_id);
    renderActivity();
  }

  dataChannel.send(JSON.stringify({
    type: "conversation.item.create",
    item: {
      type: "function_call_output",
      call_id: call.call_id,
      output: JSON.stringify(result),
    },
  }));

  dataChannel.send(JSON.stringify({ type: "response.create" }));
}

function addTranscriptEntry(role, text) {
  transcript.push({ role, text, at: new Date().toISOString() });

  transcriptEmptyEl.hidden = true;

  const li = document.createElement("li");
  li.className = `role-${role}`;

  const label = document.createElement("span");
  label.className = "role-label";
  label.textContent = role === "user" ? "You" : "Agent";

  const body = document.createElement("span");
  body.className = "entry-text";
  body.textContent = text;

  li.append(label, body);
  transcriptLogEl.appendChild(li);
  transcriptLogEl.scrollTop = transcriptLogEl.scrollHeight;

  downloadBtn.hidden = false;
}

function downloadTranscript() {
  const blob = new Blob([JSON.stringify(transcript, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "transcript.json";
  link.click();

  URL.revokeObjectURL(url);
}
