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
