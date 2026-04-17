from redis import Redis

from memory_dropbox.config import settings


def get_redis() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)

