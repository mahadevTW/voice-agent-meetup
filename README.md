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

`notebook/voice_utils.py` has two reusable helpers used throughout the
notebook: `record_audio(filename, duration)` records from the mic to a WAV
file, `play_audio(filename)` plays a WAV file through the speakers. Both use
`sounddevice`/`soundfile` — grant terminal/Jupyter microphone access when the
OS prompts.

```bash
jupyter notebook notebook/voice_ai_meetup.ipynb
```

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
