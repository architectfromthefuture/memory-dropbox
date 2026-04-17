import json
from uuid import UUID

from memory_dropbox.cache.redis_client import get_redis


INDEX_QUEUE_KEY = "memory_dropbox:index_queue"


def enqueue_index_job(item_id: UUID) -> None:
    client = get_redis()
    payload = json.dumps({"item_id": str(item_id)})
    client.lpush(INDEX_QUEUE_KEY, payload)


def pop_index_job(block_timeout_s: int = 5) -> dict | None:
    client = get_redis()
    result = client.brpop(INDEX_QUEUE_KEY, timeout=block_timeout_s)
    if not result:
        return None
    _, payload = result
    return json.loads(payload)

