from threading import Thread
from typing import Any

from wikidata_producer.daemon import *
from wikidata_producer.interchange import *


class InMemoryCache(ChecksumCache):
    content = dict()

    def get_message_type(self, battle_event: BattleEvent) -> KafkaMessageType:
        existing_checksum = self.content.get(battle_event.id)
        if existing_checksum is None:
            return KafkaMessageType.NewBattle
        return KafkaMessageType.BattleUpdate

    def save_checksum_with_id(self, battle_event: BattleEvent) -> None:
        self.content[battle_event.id] = battle_event.checksum


class OfflineWikidataSource(WikidataSource):
    def __init__(self, battle_events: list[BattleEvent]) -> None:
        self.battle_events = battle_events

    def get_battle_events(
        self,
        date_start: str,
        date_end: str,
        limit: int | None = None,
    ) -> list[BattleEvent]:
        return self.battle_events[:limit]


class OfflineProducer:
    def __init__(self) -> None:
        self.products: list[KafkaMessage] = []

    def produce(self, payload: KafkaMessage) -> None:
        self.products.append(payload)
    
    def flush(self) -> None:
        pass  # noqa: WPS420


def test_daemon() -> None:
    battle_events = [
        BattleEvent(
            id="a",
            name="",
            date=0,
            location="",
            wikipedia_url_stub="",
            coordinates="",
            outcome="",
            image_url_stub="",
        ),
        BattleEvent(
            id="a",
            name="",
            date=0,
            location="New location",
            wikipedia_url_stub="",
            coordinates="",
            outcome="",
            image_url_stub="",
        ),
    ]
    producer = OfflineProducer()
    wikidata = OfflineWikidataSource(battle_events=battle_events)
    checksum_cache = InMemoryCache()
    daemon = WikidataProducerDaemon(
        producer=producer,
        wikidata=wikidata,
        checksum_cache=checksum_cache,
        sleep_interval_seconds=0,
        batch_size=2,
    )

    daemon.tick()

    assert len(producer.products) == 2
    assert producer.products[0].message_type.value == KafkaMessageType.NewBattle.value
    assert producer.products[1].message_type.value == KafkaMessageType.BattleUpdate.value
