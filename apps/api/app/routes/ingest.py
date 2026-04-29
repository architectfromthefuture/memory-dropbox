from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.deps import get_db
from memory_dropbox.events.emitter import emit_event
from memory_dropbox.events.types import FILE_INGESTED
from memory_dropbox.repositories.items import create_item
from memory_dropbox.schemas.items import ItemCreate, ItemRead
from memory_dropbox.search.hybrid import item_to_read
from memory_dropbox.services.indexing import create_index_job


router = APIRouter()


@router.post(
    "/text",
    response_model=ItemRead,
    summary="Ingest pasted text",
    description="Creates one memory item from JSON (title, body, tags, …) and enqueues indexing.",
)
async def ingest_text(payload: ItemCreate, db: Session = Depends(get_db)):
    item = create_item(db, payload, source_type="paste")
    create_index_job(db, item)
    return item_to_read(item)


@router.post(
    "/file",
    response_model=list[ItemRead],
    summary="Ingest a text-like file",
    description=(
        "Reads the uploaded bytes as UTF-8 (invalid sequences ignored) and splits on blank lines "
        "into separate memory items. Intended for plain text and Markdown (`.txt`, `.md`). "
        "PDF and other binary formats are not parsed here—use a dedicated extractor or connector "
        "(e.g. a pdf-intelligence pipeline) when you add document extraction."
    ),
)
async def ingest_file(
    file: UploadFile = File(...),
    kind: str = Form(default="note"),
    tags: str = Form(default=""),
    db: Session = Depends(get_db),
):
    raw = (await file.read()).decode("utf-8", errors="ignore")
    chunks = [s.strip() for s in raw.split("\n\n") if s.strip()]
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    created: list[ItemRead] = []
    for i, chunk in enumerate(chunks, start=1):
        payload = ItemCreate(
            title=f"{file.filename} part {i}",
            body=chunk,
            tags=tag_list,
            kind=kind,
            metadata={"filename": file.filename},
        )
        item = create_item(db, payload, source_type="upload")
        create_index_job(db, item)
        created.append(item_to_read(item))
    emit_event(
        FILE_INGESTED,
        {
            "filename": file.filename or "",
            "chunk_count": len(created),
            "item_ids": [str(item.id) for item in created],
        },
    )
    return created

