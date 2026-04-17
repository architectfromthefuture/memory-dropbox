import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from memory_dropbox.db.models import DerivedMemory, Event, IngestionMemory, ObservationMemory
from memory_dropbox.db.session import SessionLocal
from memory_dropbox.events.types import FILE_INGESTED, EventPayload, EventType

FILE_INGESTED_OBSERVATION_TYPE = "file_ingested_observation"


def add_derived_memories_for_event(
    db: Session,
    event_type: EventType,
    payload: EventPayload,
    source_event_id: uuid.UUID | None = None,
) -> None:
    if event_type != FILE_INGESTED:
        return

    raw_chunk_count = payload.get("chunk_count", 0)
    chunk_count = int(raw_chunk_count) if isinstance(raw_chunk_count, int | str) else 0
    filename = str(payload.get("filename", ""))
    db.add(
        DerivedMemory(
            source_event_id=source_event_id,
            event_type=event_type,
            filename=filename,
            chunk_count=chunk_count,
        )
    )
    if source_event_id is not None:
        # observation_type tokens should stay stable and deterministic across runs.
        db.add(
            ObservationMemory(
                observation_type=FILE_INGESTED_OBSERVATION_TYPE,
                content=f"File '{filename}' was ingested and split into {chunk_count} chunks.",
                filename=filename,
                chunk_count=chunk_count,
                source_event_id=source_event_id,
            )
        )

    ingestion_memory = db.scalars(
        select(IngestionMemory).where(IngestionMemory.filename == filename).limit(1)
    ).first()
    ingested_at = datetime.now(timezone.utc)
    if ingestion_memory is None:
        db.add(
            IngestionMemory(
                filename=filename,
                total_chunks=chunk_count,
                ingestion_count=1,
                last_ingested_at=ingested_at,
            )
        )
    else:
        ingestion_memory.ingestion_count += 1
        ingestion_memory.total_chunks = chunk_count
        ingestion_memory.last_ingested_at = ingested_at
        db.add(ingestion_memory)


def get_recent_derived_memories_with_source_event_context(
    limit: int = 100,
) -> list[dict[str, object | None]]:
    stmt = (
        select(DerivedMemory, Event)
        .outerjoin(Event, DerivedMemory.source_event_id == Event.id)
        .order_by(DerivedMemory.timestamp.desc())
        .limit(limit)
    )
    with SessionLocal() as db:
        rows = db.execute(stmt).all()

    return [
        {
            "derived_memory_id": str(derived.id),
            "event_type": derived.event_type,
            "filename": derived.filename,
            "chunk_count": derived.chunk_count,
            "derived_timestamp": derived.timestamp.isoformat(),
            "source_event_id": str(derived.source_event_id) if derived.source_event_id else None,
            "source_event_type": source_event.event_type if source_event else None,
            "source_event_payload": source_event.payload if source_event else None,
            "source_event_timestamp": source_event.timestamp.isoformat() if source_event else None,
        }
        for derived, source_event in rows
    ]


def get_recent_observation_memories_with_source_event_context(
    limit: int = 100,
) -> list[dict[str, object | None]]:
    stmt = (
        select(ObservationMemory, Event)
        .outerjoin(Event, ObservationMemory.source_event_id == Event.id)
        .order_by(ObservationMemory.timestamp.desc())
        .limit(limit)
    )
    with SessionLocal() as db:
        rows = db.execute(stmt).all()

    return [
        {
            "observation_memory_id": str(observation.id),
            "observation_type": observation.observation_type,
            "content": observation.content,
            "filename": observation.filename,
            "chunk_count": observation.chunk_count,
            "observation_timestamp": observation.timestamp.isoformat(),
            "source_event_id": str(observation.source_event_id),
            "source_event_type": source_event.event_type if source_event else None,
            "source_event_payload": source_event.payload if source_event else None,
            "source_event_timestamp": source_event.timestamp.isoformat() if source_event else None,
        }
        for observation, source_event in rows
    ]


def get_recent_memory_activity(limit: int = 100) -> list[dict[str, object | None]]:
    if limit <= 0:
        return []

    with SessionLocal() as db:
        events = db.scalars(select(Event).order_by(Event.timestamp.desc()).limit(limit)).all()
        derived_memories = db.scalars(
            select(DerivedMemory).order_by(DerivedMemory.timestamp.desc()).limit(limit)
        ).all()
        observation_memories = db.scalars(
            select(ObservationMemory).order_by(ObservationMemory.timestamp.desc()).limit(limit)
        ).all()

    activity_rows: list[tuple[datetime, dict[str, object | None]]] = []

    for event in events:
        activity_rows.append(
            (
                event.timestamp,
                {
                    "record_type": "event",
                    "subtype": event.event_type,
                    "timestamp": event.timestamp.isoformat(),
                    "source_event_id": None,
                    "summary_text": f"Event '{event.event_type}' emitted.",
                    "filename": str(event.payload.get("filename", "")) if isinstance(event.payload, dict) else None,
                    "chunk_count": (
                        int(event.payload.get("chunk_count", 0))
                        if isinstance(event.payload, dict)
                        and isinstance(event.payload.get("chunk_count"), int | str)
                        else None
                    ),
                },
            )
        )

    for derived in derived_memories:
        activity_rows.append(
            (
                derived.timestamp,
                {
                    "record_type": "derived_memory",
                    "subtype": derived.event_type,
                    "timestamp": derived.timestamp.isoformat(),
                    "source_event_id": str(derived.source_event_id) if derived.source_event_id else None,
                    "summary_text": (
                        f"Derived memory from '{derived.event_type}' "
                        f"for file '{derived.filename}' with {derived.chunk_count} chunks."
                    ),
                    "filename": derived.filename,
                    "chunk_count": derived.chunk_count,
                },
            )
        )

    for observation in observation_memories:
        activity_rows.append(
            (
                observation.timestamp,
                {
                    "record_type": "observation_memory",
                    "subtype": observation.observation_type,
                    "timestamp": observation.timestamp.isoformat(),
                    "source_event_id": str(observation.source_event_id),
                    "summary_text": observation.content,
                    "filename": observation.filename,
                    "chunk_count": observation.chunk_count,
                },
            )
        )

    activity_rows.sort(key=lambda row: row[0], reverse=True)
    return [row[1] for row in activity_rows[:limit]]
