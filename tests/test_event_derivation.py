"""Derivation helpers without a live integration DB."""

from unittest.mock import MagicMock

from memory_dropbox.events.derive_memory import FILE_INGESTED_OBSERVATION_TYPE, add_derived_memories_for_event
from memory_dropbox.events.types import INDEXING_COMPLETED


def test_add_derived_memories_skips_non_file_ingested_events() -> None:
    db = MagicMock()
    add_derived_memories_for_event(db, INDEXING_COMPLETED, {})
    db.add.assert_not_called()


def test_file_ingested_observation_type_token() -> None:
    assert FILE_INGESTED_OBSERVATION_TYPE == "file_ingested_observation"
