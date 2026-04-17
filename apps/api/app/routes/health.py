from fastapi import APIRouter
from sqlalchemy import text

from memory_dropbox.cache.redis_client import get_redis
from memory_dropbox.db.session import SessionLocal
from memory_dropbox.vector.qdrant_store import get_client


router = APIRouter()


@router.get("")
async def health_root():
    services = {"postgres": "down", "redis": "down", "qdrant": "down"}

    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        services["postgres"] = "up"
    except Exception:
        pass

    try:
        get_redis().ping()
        services["redis"] = "up"
    except Exception:
        pass

    try:
        get_client().get_collections()
        services["qdrant"] = "up"
    except Exception:
        pass

    status = "ok" if all(v == "up" for v in services.values()) else "degraded"
    return {"status": status, "services": services}

