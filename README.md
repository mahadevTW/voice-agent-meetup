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

`notebook/voice_ai_meetup.ipynb` carries the talking points and agenda for the
full 2-hour session, plus small live-code snippets (a traditional STT→LLM→TTS
pipeline run end-to-end on a real mic recording, the realtime event list, a
direct `/tools/call` request). Walk through it, then switch to the browser at
the "Live Demo Break" section for the actual end-to-end voice demo.

The notebook's first code cell defines two reusable helpers used throughout:
`record_audio(filename, duration)` records from the mic to a WAV file,
`play_audio(filename)` plays a WAV file through the speakers. Both use
`sounddevice`/`soundfile` — grant terminal/Jupyter microphone access when the
OS prompts.

```bash
jupyter notebook notebook/voice_ai_meetup.ipynb
```

### Workshop sequence

Full detail lives in [`voice-agent.md`](./voice-agent.md); this is the order
to run through on the day:

1. **Why Voice AI** (0–10 min) — the interface-shift narrative, then ask the
   room "why is voice harder than chat?"
2. **Traditional pipeline — naive version** (10–20 min) — STT → LLM → TTS,
   run live in the notebook on a real mic recording, timed. Drawbacks only
   hold if implemented naively.
3. **Production reality: modular vs unified** (20–35 min) — how production
   voice AI companies actually solve latency (streaming STT/LLM/TTS, parallel
   tool calls, VAD), then present Modular Stack vs Realtime as two valid
   architectures with real trade-offs, not "realtime always wins."
4. **Realtime API concepts & event model** (35–50 min) — session, events,
   audio chunks, conversation state, streaming responses.
5. **Live demo break — hands-on** (50–90 min) — switch to this repo's browser
   app (`uvicorn backend.main:app --reload`), build up session → connect →
   mic → send/receive audio → playback, step by step.
6. **Tool calling** (90–110 min) — walk through `get_weather` /
   `calculate` / `get_order_status`, then call `/tools/call` directly from
   the notebook against the running server.
7. **Prompt engineering, advanced features, Q&A** (110–120 min) — voice
   prompting rules, a mention-only pass over VAD/interruptions/multi-language,
   then the closing end-to-end demo flow.

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
