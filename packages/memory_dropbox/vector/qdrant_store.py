from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from memory_dropbox.config import settings


def get_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


def ensure_collection() -> None:
    client = get_client()
    collections = client.get_collections().collections
    if not any(c.name == settings.qdrant_collection for c in collections):
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=settings.embedding_dim, distance=Distance.COSINE),
        )


def upsert_item_vector(item_id: str, vector: list[float], payload: dict) -> None:
    client = get_client()
    ensure_collection()
    client.upsert(
        collection_name=settings.qdrant_collection,
        points=[PointStruct(id=item_id, vector=vector, payload=payload)],
    )


def semantic_search(vector: list[float], limit: int = 10):
    client = get_client()
    ensure_collection()
    return client.search(collection_name=settings.qdrant_collection, query_vector=vector, limit=limit)

