# Voice Agent Meetup

Minimal browser-based voice agent built on the OpenAI Realtime API, for the
2-hour workshop described in [`voice-agent.md`](./voice-agent.md).

Vanilla JS + WebRTC on the frontend, FastAPI on the backend. Three toy tools
(`get_weather`, `calculate`, `get_order_status`) demonstrate function calling.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in OPENAI_API_KEY
```

## Run

```bash
uvicorn backend.main:app --reload
```

Open http://localhost:8000 and click "Start talking".

## Presenting the workshop

The talking points and agenda are split across three notebooks in
`notebook/`, run in order — each one ends by handing off to the next:

| Notebook | Covers | Agenda slot |
|---|---|---|
| [`01_basic_stt_tts.ipynb`](notebook/01_basic_stt_tts.ipynb) | Why voice AI, the naive STT→LLM→TTS pipeline run live on a real mic recording, timed | 0–20 min |
| [`02_optimized_streaming.ipynb`](notebook/02_optimized_streaming.ipynb) | Why the naive pipeline is slow; live streaming STT with real VAD turn-detection (`gpt-4o-transcribe` over the Realtime API) → streaming LLM → streaming TTS, first shown stage-by-stage then wired into an actual multi-turn `voice_loop()` that listens → responds → listens again, skipping the LLM/TTS call entirely on silence; the 5 production optimizations; Modular vs Unified architecture comparison | 20–35 min |
| [`03_gpt_realtime.ipynb`](notebook/03_gpt_realtime.ipynb) | Realtime session/event model, hands-off to the browser app, tool calling via a direct `/tools/call` request, prompt engineering, Q&A | 35–120 min |

`01_basic_stt_tts.ipynb`'s first code cell defines two reusable helpers used
in that notebook: `record_audio(filename, duration)` records from the mic to
a WAV file, `play_audio(filename)` plays a WAV file through the speakers.
Both use `sounddevice`/`soundfile` — grant terminal/Jupyter microphone access
when the OS prompts.

```bash
jupyter notebook notebook/01_basic_stt_tts.ipynb
```

### Workshop sequence

Full detail lives in [`voice-agent.md`](./voice-agent.md); this is the order
to run through on the day:

1. **Why Voice AI** (0–10 min, `01_basic_stt_tts.ipynb`) — the interface-shift
   narrative, then ask the room "why is voice harder than chat?"
2. **Traditional pipeline — naive version** (10–20 min, `01_basic_stt_tts.ipynb`)
   — STT → LLM → TTS, run live on a real mic recording, timed. Drawbacks only
   hold if implemented naively.
3. **Production reality: modular vs unified** (20–35 min, `02_optimized_streaming.ipynb`)
   — how production voice AI companies actually solve latency: live streaming
   STT with real server-side VAD (partial transcript prints *while you're
   still talking*, turn ends on an actual pause, not a fixed timer; no speech
   detected → no LLM call at all), chained into streaming LLM and streaming
   TTS. Then present Modular Stack vs Realtime as two valid architectures
   with real trade-offs, not "realtime always wins."
4. **Realtime API concepts & event model** (35–50 min, `03_gpt_realtime.ipynb`)
   — session, events, audio chunks, conversation state, streaming responses.
5. **Live demo break — hands-on** (50–90 min) — switch to this repo's browser
   app (`uvicorn backend.main:app --reload`), build up session → connect →
   mic → send/receive audio → playback, step by step.
6. **Tool calling** (90–110 min, `03_gpt_realtime.ipynb`) — walk through
   `get_weather` / `calculate` / `get_order_status`, then call `/tools/call`
   directly from the notebook against the running server.
7. **Prompt engineering, advanced features, Q&A** (110–120 min, `03_gpt_realtime.ipynb`)
   — voice prompting rules, a mention-only pass over
   VAD/interruptions/multi-language, then the closing end-to-end demo flow.

## Layout

```
backend/
  main.py              # FastAPI app entrypoint
  api/
    frontend.py         # serves index.html
    realtime.py          # POST /realtime/session — ephemeral token + tool schemas
    tools.py             # POST /tools/call — dispatches get_weather/calculate/get_order_status
  core/
    config.py            # env vars, model/voice settings
    agent-instruction.md # system prompt
  templates/index.html
  static/{app.js,style.css}
```

Add new tools by writing a handler in `backend/api/tools.py`, registering it in
`TOOL_HANDLERS`, and adding its schema to `REALTIME_TOOLS` in
`backend/api/realtime.py`.
