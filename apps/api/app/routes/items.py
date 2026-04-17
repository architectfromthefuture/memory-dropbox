from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.deps import get_db
from memory_dropbox.repositories.items import get_item, list_items, update_item
from memory_dropbox.schemas.items import ItemRead, ItemUpdate
from memory_dropbox.search.hybrid import item_to_read


router = APIRouter()


@router.get("", response_model=list[ItemRead])
def get_items(limit: int = 50, db: Session = Depends(get_db)):
    return [item_to_read(item) for item in list_items(db, limit=limit)]


@router.get("/{item_id}", response_model=ItemRead)
def get_item_by_id(item_id: UUID, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_to_read(item)


@router.patch("/{item_id}", response_model=ItemRead)
def patch_item(item_id: UUID, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = update_item(db, item, payload)
    return item_to_read(updated)


@router.post("/{item_id}/tags", response_model=ItemRead)
def add_tags(item_id: UUID, tags: list[str], db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    merged = sorted({*(t.name for t in item.tags), *(t.strip().lower() for t in tags if t.strip())})
    updated = update_item(db, item, ItemUpdate(tags=merged))
    return item_to_read(updated)


@router.get("/export/json")
def export_items_json(limit: int = 100, db: Session = Depends(get_db)):
    items = [item_to_read(item).model_dump(mode="json") for item in list_items(db, limit=limit)]
    return {"items": items}


@router.get("/export/markdown", response_class=PlainTextResponse)
def export_items_markdown(limit: int = 100, db: Session = Depends(get_db)):
    lines = ["# Memory Dropbox Export", ""]
    for item in list_items(db, limit=limit):
        lines.append(f"## {item.title}")
        lines.append(f"- id: `{item.id}`")
        lines.append(f"- kind: `{item.kind}`")
        if item.tags:
            lines.append(f"- tags: {', '.join(t.name for t in item.tags)}")
        lines.append("")
        lines.append(item.body)
        lines.append("")
    return "\n".join(lines)

