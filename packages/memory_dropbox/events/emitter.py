import logging
from sqlalchemy import select

from memory_dropbox.db.models import DerivedMemory, Event
from memory_dropbox.db.session import SessionLocal
from memory_dropbox.events.derive_memory import add_derived_memories_for_event
from memory_dropbox.events.types import EventPayload, EventRecord, EventType

logger = logging.getLogger("memory_dropbox.events")

_emitted_events: list[EventRecord] = []


def emit_event(event_type: EventType, payload: EventPayload | None = None) -> EventRecord:
    event: EventRecord = {"type": event_type, "payload": payload or {}}
    _emitted_events.append(event)
    try:
        with SessionLocal() as db:
            event_row = Event(event_type=event_type, payload=event["payload"])
            db.add(event_row)
            db.flush()
            add_derived_memories_for_event(
                db,
                event_type,
                event["payload"],
                source_event_id=event_row.id,
            )
            db.commit()
    except Exception:
        logger.exception("event_persist_failed type=%s", event_type)
    logger.info("event_emitted type=%s payload=%s", event_type, event["payload"])
    return event


def get_emitted_events() -> list[EventRecord]:
    return list(_emitted_events)


def clear_emitted_events() -> None:
    _emitted_events.clear()


def get_persisted_events(limit: int = 100) -> list[dict[str, object]]:
    with SessionLocal() as db:
        rows = db.scalars(select(Event).order_by(Event.timestamp.desc()).limit(limit)).all()
    return [
        {
            "event_type": row.event_type,
            "payload": row.payload,
            "timestamp": row.timestamp.isoformat(),
        }
        for row in rows
    ]


def get_derived_memories(limit: int = 100) -> list[dict[str, object]]:
    with SessionLocal() as db:
        rows = db.scalars(select(DerivedMemory).order_by(DerivedMemory.timestamp.desc()).limit(limit)).all()
    return [
        {
            "event_type": row.event_type,
            "filename": row.filename,
            "chunk_count": row.chunk_count,
            "timestamp": row.timestamp.isoformat(),
        }
        for row in rows
    ]
