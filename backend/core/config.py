import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REALTIME_MODEL = os.getenv("REALTIME_MODEL", "gpt-realtime-2.1")
REALTIME_VOICE = os.getenv("REALTIME_VOICE", "marin")
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")
TRANSCRIPTION_LANGUAGE = os.getenv("TRANSCRIPTION_LANGUAGE", "en")

AGENT_INSTRUCTIONS_PATH = Path(__file__).parent / "agent-instruction.md"
AGENT_INSTRUCTIONS = os.getenv(
    "AGENT_INSTRUCTIONS",
    AGENT_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
)
