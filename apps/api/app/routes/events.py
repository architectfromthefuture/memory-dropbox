"""Public event log JSON."""

from fastapi import APIRouter

from memory_dropbox.events.emitter import get_persisted_events

router = APIRouter(tags=["events"])


@router.get("/events")
def list_events(limit: int = 50) -> dict[str, object]:
    lim = max(1, min(limit, 200))
    return {"events": get_persisted_events(lim)}
