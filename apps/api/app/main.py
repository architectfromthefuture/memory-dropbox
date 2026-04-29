from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from memory_dropbox.logging import configure_logging
from memory_dropbox.vector.qdrant_store import ensure_collection

from app.routes import events, health, home, ingest, items, memory, search


def create_app() -> FastAPI:
    configure_logging()

    api = FastAPI(title="Memory Dropbox", version="0.1.0")
    api.include_router(home.router)
    api.include_router(health.router, prefix="/health")
    api.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
    api.include_router(items.router, prefix="/items", tags=["items"])
    api.include_router(search.router, prefix="/search", tags=["search"])
    api.include_router(events.router)
    api.include_router(memory.router, prefix="/memory", tags=["memory"])

    _static_dir = Path(__file__).resolve().parent.parent / "static"
    if _static_dir.is_dir():
        api.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

    @api.on_event("startup")
    async def startup_event() -> None:
        try:
            ensure_collection()
        except Exception:
            # Keep startup tolerant while services warm up.
            pass

    return api


app = create_app()
