import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.frontend import router as frontend_router
from backend.api.realtime import router as realtime_router
from backend.api.tools import router as tools_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Voice Agent Meetup")

app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "static")),
    name="static",
)

app.include_router(frontend_router)
app.include_router(realtime_router)
app.include_router(tools_router)


@app.get("/health")
def health():
    return {"status": "ok"}
