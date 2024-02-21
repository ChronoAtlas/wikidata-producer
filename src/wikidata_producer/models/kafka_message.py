import json
from typing import Generic, TypeVar

from wikidata_producer.models.json_serializable import JsonSerializable

ContentModel = TypeVar("ContentModel", bound=JsonSerializable)


class KafkaMessage(Generic[ContentModel], JsonSerializable):
    content: ContentModel
    message_type: str

    def __init__(self, content: ContentModel, message_type: str) -> None:
        self.content = content
        self.message_type = message_type

    def json(self) -> str:
        return json.dumps(
            {
                "content": self.content.json(),
                "message_type": self.message_type,
            }
        )
