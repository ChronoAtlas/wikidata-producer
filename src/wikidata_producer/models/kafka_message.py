from typing import Any, Generic, TypeVar

from wikidata_producer.models import *

ContentModel = TypeVar("ContentModel", bound=JsonSerializable)


class KafkaMessage(Generic[ContentModel], JsonSerializable):
    content: ContentModel
    message_type: str

    def __init__(self, content: ContentModel, message_type: str) -> None:
        self.content = content
        self.message_type = message_type

    def json(self) -> dict[str, Any]:
        return {
            "content": self.content.json(),
            "message_type": self.message_type.value,
        }
