import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REALTIME_MODEL = os.getenv("REALTIME_MODEL", "gpt-realtime-2.1")
REALTIME_VOICE = os.getenv("REALTIME_VOICE", "marin")
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")
TRANSCRIPTION_LANGUAGE = os.getenv("TRANSCRIPTION_LANGUAGE", "en")

# Base URL of the locally-running ecommerce-demo REST API (see
# build-your-mcp-server-public/ecommerce-demo). Configurable since that
# service can be run on any port.
SHOPPING_API_BASE_URL = os.getenv("SHOPPING_API_BASE_URL", "http://localhost:8000").rstrip("/")

AGENT_INSTRUCTIONS_PATH = Path(__file__).parent / "agent-instruction.md"
AGENT_INSTRUCTIONS = os.getenv(
    "AGENT_INSTRUCTIONS",
    AGENT_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
)

POLICIES_DIR = Path(__file__).resolve().parent.parent.parent / "policies"
