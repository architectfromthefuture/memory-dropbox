"""Event type constants stay wired for persistence and OpenAPI."""

from memory_dropbox.events.types import FILE_INGESTED, INDEXING_COMPLETED


def test_known_event_types_are_stable_strings() -> None:
    assert FILE_INGESTED == "file_ingested"
    assert INDEXING_COMPLETED == "indexing_completed"
