from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from memory_dropbox.db.models import Item
from memory_dropbox.repositories.items import get_item
from memory_dropbox.schemas.items import ItemRead, SearchResult
from memory_dropbox.vector.embeddings import embed_text
from memory_dropbox.vector.qdrant_store import semantic_search


@dataclass
class WeightedScore:
    keyword: float = 0.0
    semantic: float = 0.0

    @property
    def total(self) -> float:
        return self.keyword * 0.45 + self.semantic * 0.55


def item_to_read(item: Item) -> ItemRead:
    return ItemRead(
        id=item.id,
        created_at=item.created_at,
        updated_at=item.updated_at,
        title=item.title,
        body=item.body,
        source_url=item.source_url,
        kind=item.kind,
        metadata=item.metadata_json or {},
        tags=[t.name for t in item.tags],
    )


def keyword_search(db: Session, query: str, limit: int = 10) -> list[SearchResult]:
    stmt = text(
        """
        SELECT id, ts_rank_cd(to_tsvector('english', title || ' ' || body), plainto_tsquery('english', :q)) as rank
        FROM items
        WHERE to_tsvector('english', title || ' ' || body) @@ plainto_tsquery('english', :q)
        ORDER BY rank DESC
        LIMIT :limit
        """
    )
    rows = db.execute(stmt, {"q": query, "limit": limit}).all()
    results: list[SearchResult] = []
    for row in rows:
        item = get_item(db, row.id)
        if item:
            results.append(SearchResult(item=item_to_read(item), score=float(row.rank), source="keyword"))
    return results


def semantic_query(db: Session, query: str, limit: int = 10) -> list[SearchResult]:
    vector = embed_text(query)
    hits = semantic_search(vector, limit=limit)
    results: list[SearchResult] = []
    for hit in hits:
        item = get_item(db, UUID(str(hit.id)))
        if item:
            results.append(SearchResult(item=item_to_read(item), score=float(hit.score), source="semantic"))
    return results


def hybrid_search(db: Session, query: str, limit: int = 10) -> list[SearchResult]:
    k_results = keyword_search(db, query, limit=limit)
    s_results = semantic_query(db, query, limit=limit)
    scores: dict[UUID, WeightedScore] = {}

    for result in k_results:
        scores.setdefault(result.item.id, WeightedScore()).keyword = result.score
    for result in s_results:
        scores.setdefault(result.item.id, WeightedScore()).semantic = result.score

    ranked = sorted(scores.items(), key=lambda x: x[1].total, reverse=True)[:limit]
    output: list[SearchResult] = []
    for item_id, score in ranked:
        item = get_item(db, item_id)
        if item:
            output.append(SearchResult(item=item_to_read(item), score=score.total, source="hybrid"))
    return output

