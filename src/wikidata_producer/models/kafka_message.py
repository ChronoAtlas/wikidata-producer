from typing import Any

from wikidata_producer.models.battle_event import BattleEvent


class KafkaMessage:
    battle_event: BattleEvent
    message_type: str

    def __init__(self, body: BattleEvent, message_type: str) -> None:
        self.id = body.id
        self.battle_event = body
        self.message_type = message_type

    @property
    def __dict__(self) -> dict[str, Any]:  # type: ignore
        return {
            "id": self.battle_event.id,
            "body": self.battle_event.__dict__,
            "message_type": self.message_type,
        }
