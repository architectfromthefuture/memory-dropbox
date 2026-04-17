from __future__ import annotations

from sqlalchemy.orm import Session

from memory_dropbox.db.models import IndexJob, Item
from memory_dropbox.queue.jobs import enqueue_index_job


def create_index_job(db: Session, item: Item) -> IndexJob:
    job = IndexJob(item_id=item.id, status="queued")
    db.add(job)
    db.commit()
    enqueue_index_job(item.id)
    return job

