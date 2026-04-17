import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from memory_dropbox.cache.redis_client import get_redis
from memory_dropbox.schemas.items import SearchResult
from memory_dropbox.search.hybrid import hybrid_search, keyword_search, semantic_query


router = APIRouter()


def _cached(key: str):
    try:
        raw = get_redis().get(key)
    except Exception:
        return None
    if not raw:
        return None
    return [SearchResult(**entry) for entry in json.loads(raw)]


def _set_cache(key: str, value: list[SearchResult], ttl_s: int = 120):
    try:
        payload = [entry.model_dump(mode="json") for entry in value]
        get_redis().setex(key, ttl_s, json.dumps(payload))
    except Exception:
        return


@router.get("", response_model=list[SearchResult])
def search(query: str, limit: int = 10, db: Session = Depends(get_db)):
    key = f"search:keyword:{query}:{limit}"
    cached = _cached(key)
    if cached is not None:
        return cached
    result = keyword_search(db, query=query, limit=limit)
    _set_cache(key, result)
    return result


@router.get("/semantic", response_model=list[SearchResult])
def search_semantic(query: str, limit: int = 10, db: Session = Depends(get_db)):
    key = f"search:semantic:{query}:{limit}"
    cached = _cached(key)
    if cached is not None:
        return cached
    result = semantic_query(db, query=query, limit=limit)
    _set_cache(key, result)
    return result


@router.get("/hybrid", response_model=list[SearchResult])
def search_hybrid(query: str, limit: int = 10, db: Session = Depends(get_db)):
    key = f"search:hybrid:{query}:{limit}"
    cached = _cached(key)
    if cached is not None:
        return cached
    result = hybrid_search(db, query=query, limit=limit)
    _set_cache(key, result)
    return result

