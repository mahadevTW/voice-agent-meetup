import logging

from fastapi import APIRouter, HTTPException

from backend.api.demo_tools import DEMO_TOOL_HANDLERS
from backend.api.helpline_tools import HELPLINE_TOOL_HANDLERS
from backend.api.shopping_tools import SHOPPING_TOOL_HANDLERS

logger = logging.getLogger("tools")

router = APIRouter()

TOOL_HANDLERS = {
    **DEMO_TOOL_HANDLERS,
    **SHOPPING_TOOL_HANDLERS,
    **HELPLINE_TOOL_HANDLERS,
}


@router.post("/tools/call")
def call_tool(payload: dict):
    """Single entrypoint for every tool call. Dispatches internally by tool name."""
    name = payload.get("name")
    args = payload.get("arguments", {})

    logger.info("tool call: name=%s args=%s", name, args)

    handler = TOOL_HANDLERS.get(name)
    if handler is None:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {name}")

    result = handler(args)
    logger.info("tool result: name=%s result=%s", name, result)

    return result
