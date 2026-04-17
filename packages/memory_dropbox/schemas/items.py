from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)
    source_url: str | None = None
    kind: str = "note"
    metadata: dict = Field(default_factory=dict)


class ItemUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    tags: list[str] | None = None
    source_url: str | None = None
    kind: str | None = None
    metadata: dict | None = None


class ItemRead(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    title: str
    body: str
    source_url: str | None
    kind: str
    metadata: dict
    tags: list[str]


class SearchResult(BaseModel):
    item: ItemRead
    score: float
    source: str

