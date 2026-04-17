from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from memory_dropbox.db.models import Ingestion, Item, ItemTag, Tag
from memory_dropbox.schemas.items import ItemCreate, ItemUpdate


def _get_or_create_tags(db: Session, names: list[str]) -> list[Tag]:
    tags: list[Tag] = []
    normalized = sorted({n.strip().lower() for n in names if n.strip()})
    if not normalized:
        return tags
    existing = db.scalars(select(Tag).where(Tag.name.in_(normalized))).all()
    by_name = {t.name: t for t in existing}
    for name in normalized:
        if name not in by_name:
            tag = Tag(name=name)
            db.add(tag)
            db.flush()
            by_name[name] = tag
        tags.append(by_name[name])
    return tags


def create_item(db: Session, payload: ItemCreate, source_type: str = "paste") -> Item:
    item = Item(
        title=payload.title,
        body=payload.body,
        source_url=payload.source_url,
        kind=payload.kind,
        metadata_json=payload.metadata,
    )
    db.add(item)
    db.flush()
    tags = _get_or_create_tags(db, payload.tags)
    for tag in tags:
        db.add(ItemTag(item_id=item.id, tag_id=tag.id))
    db.add(
        Ingestion(
            source_type=source_type,
            raw_payload=payload.model_dump(),
            status="accepted",
        )
    )
    db.commit()
    return get_item(db, item.id)


def list_items(db: Session, limit: int = 50) -> list[Item]:
    stmt = (
        select(Item)
        .options(selectinload(Item.tags))
        .order_by(Item.created_at.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get_item(db: Session, item_id) -> Item:
    stmt = select(Item).options(selectinload(Item.tags)).where(Item.id == item_id)
    return db.scalars(stmt).first()


def update_item(db: Session, item: Item, payload: ItemUpdate) -> Item:
    data = payload.model_dump(exclude_unset=True)
    tags = data.pop("tags", None)
    if "metadata" in data:
        item.metadata_json = data.pop("metadata")
    for k, v in data.items():
        setattr(item, k, v)
    if tags is not None:
        db.query(ItemTag).filter(ItemTag.item_id == item.id).delete()
        new_tags = _get_or_create_tags(db, tags)
        for tag in new_tags:
            db.add(ItemTag(item_id=item.id, tag_id=tag.id))
    db.add(item)
    db.commit()
    return get_item(db, item.id)

