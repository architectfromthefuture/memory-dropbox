from typing import Literal, TypedDict

FILE_INGESTED = "file_ingested"
INDEXING_COMPLETED = "indexing_completed"

EventType = Literal["file_ingested", "indexing_completed"]
EventPayload = dict[str, object]


class EventRecord(TypedDict):
    type: EventType
    payload: EventPayload
