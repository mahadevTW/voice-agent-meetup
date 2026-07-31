import requests
from fastapi import APIRouter, HTTPException

from backend.core.config import (
    AGENT_INSTRUCTIONS,
    OPENAI_API_KEY,
    REALTIME_MODEL,
    REALTIME_VOICE,
    TRANSCRIPTION_MODEL,
)

router = APIRouter()

OPENAI_CLIENT_SECRETS_URL = "https://api.openai.com/v1/realtime/client_secrets"

# Tool schemas the model sees. Every call is dispatched through the single
# POST /tools/call endpoint in backend/api/tools.py.
REALTIME_TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": "Evaluate a simple arithmetic expression, e.g. '12 * (3 + 4)'.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Arithmetic expression to evaluate"},
            },
            "required": ["expression"],
        },
    },
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Look up the delivery status of an order by its order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order ID, e.g. 'ORD-1023'"},
            },
            "required": ["order_id"],
        },
    },
]


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
                    "input": {"transcription": {"model": TRANSCRIPTION_MODEL}},
                    "output": {"voice": REALTIME_VOICE},
                },
            }
        },
        timeout=15,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
