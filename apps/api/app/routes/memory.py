"""REST handlers under `/memory/*`."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.deps import get_db
from memory_dropbox.db.models import Event, Item
from memory_dropbox.events import get_recent_memory_activity
from memory_dropbox.events.emitter import get_derived_memories, get_observation_memories

router = APIRouter()


@router.get("/activity")
def memory_activity_api(limit: int = 100, db: Session = Depends(get_db)) -> dict[str, object]:
    lim = max(1, min(limit, 200))
    raw_items = db.scalar(select(func.count()).select_from(Item))
    raw_events = db.scalar(select(func.count()).select_from(Event))
    activity = get_recent_memory_activity(limit=lim)
    return {
        "items": int(raw_items or 0),
        "events": int(raw_events or 0),
        "activity": activity,
    }


@router.get("/derived")
def list_derived(limit: int = 50) -> dict[str, object]:
    lim = max(1, min(limit, 200))
    return {"derived": get_derived_memories(lim)}


@router.get("/observations")
def list_observations(limit: int = 50) -> dict[str, object]:
    lim = max(1, min(limit, 200))
    return {"observations": get_observation_memories(lim)}
