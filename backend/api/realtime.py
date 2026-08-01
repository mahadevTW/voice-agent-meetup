import requests
from fastapi import APIRouter, HTTPException

from backend.api.tool_schemas import REALTIME_TOOLS
from backend.core.config import (
    AGENT_INSTRUCTIONS,
    OPENAI_API_KEY,
    REALTIME_MODEL,
    REALTIME_VOICE,
    TRANSCRIPTION_LANGUAGE,
    TRANSCRIPTION_MODEL,
)

router = APIRouter()

OPENAI_CLIENT_SECRETS_URL = "https://api.openai.com/v1/realtime/client_secrets"


@router.post("/realtime/session")
def create_realtime_session():
    """Create an ephemeral OpenAI Realtime client secret and hand it to the frontend."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set in the backend .env")

    response = requests.post(
        OPENAI_CLIENT_SECRETS_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "session": {
                "type": "realtime",
                "model": REALTIME_MODEL,
                "instructions": AGENT_INSTRUCTIONS,
                "tools": REALTIME_TOOLS,
                "tool_choice": "auto",
                "audio": {
                    "input": {"transcription": {"model": TRANSCRIPTION_MODEL, "language": TRANSCRIPTION_LANGUAGE}},
                    "output": {"voice": REALTIME_VOICE},
                },
            }
        },
        timeout=15,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
