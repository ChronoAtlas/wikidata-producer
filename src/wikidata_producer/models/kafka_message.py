import logging
from typing import Any, Generic, TypeVar

ContentModel = TypeVar("ContentModel")


class KafkaMessage(Generic[ContentModel]):
    body: ContentModel
    message_type: str

    def __init__(self, body: ContentModel, message_type: str) -> None:
        self.body = body
        self.message_type = message_type

    @property
    def __dict__(self) -> dict[str, Any]:
        logging.fatal(self.body.__dict__)
        return {
            "body": self.body.__dict__,
            "message_type": self.message_type,
        }
