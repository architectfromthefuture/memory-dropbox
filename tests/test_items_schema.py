"""Pydantic contracts for API payloads."""

import pytest
from pydantic import ValidationError

from memory_dropbox.schemas.items import ItemCreate


def test_item_create_rejects_empty_body() -> None:
    with pytest.raises(ValidationError):
        ItemCreate(title="only-title", body="")


def test_item_create_defaults() -> None:
    model = ItemCreate(title="t", body="content")
    assert model.kind == "note"
    assert model.tags == []
