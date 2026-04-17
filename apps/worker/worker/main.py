import logging
import time
from uuid import UUID

from memory_dropbox.logging import configure_logging
from memory_dropbox.db.models import IndexJob, Item
from memory_dropbox.db.session import SessionLocal
from memory_dropbox.events.emitter import emit_event
from memory_dropbox.events.types import INDEXING_COMPLETED
from memory_dropbox.queue.jobs import pop_index_job
from memory_dropbox.vector.embeddings import embed_text
from memory_dropbox.vector.qdrant_store import upsert_item_vector


logger = logging.getLogger("worker")


def main() -> None:
    configure_logging()
    while True:
        message = pop_index_job(block_timeout_s=5)
        if not message:
            continue

        item_id = UUID(message["item_id"])
        with SessionLocal() as db:
            item = db.get(Item, item_id)
            if not item:
                logger.warning("item not found: %s", item_id)
                continue
            job = (
                db.query(IndexJob)
                .filter(IndexJob.item_id == item_id, IndexJob.status == "queued")
                .order_by(IndexJob.created_at.asc())
                .first()
            )
            if not job:
                continue

            try:
                job.status = "processing"
                job.attempts += 1
                db.add(job)
                db.commit()

                vector = embed_text(f"{item.title}\n\n{item.body}")
                upsert_item_vector(
                    item_id=str(item.id),
                    vector=vector,
                    payload={"title": item.title, "kind": item.kind},
                )
                job.status = "completed"
                job.error = None
                db.add(job)
                db.commit()
                emit_event(
                    INDEXING_COMPLETED,
                    {"item_id": str(item.id), "job_id": str(job.id), "status": job.status},
                )
                logger.info("indexed item=%s", item.id)
            except Exception as exc:
                job.status = "failed"
                job.error = str(exc)
                db.add(job)
                db.commit()
                logger.exception("failed indexing item=%s", item.id)
                time.sleep(1)


if __name__ == "__main__":
    main()

