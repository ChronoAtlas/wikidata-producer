import json
from typing import Any

from wikidata_producer.daemon import WikidataProducerDaemon
from wikidata_producer.interchange import ChecksumCache
from wikidata_producer.interchange import Producer
from wikidata_producer.interchange import WikidataSource
from wikidata_producer.models import BattleEvent
from wikidata_producer.models import KafkaMessage
from wikidata_producer.models import KafkaMessageType


class InMemoryCache(ChecksumCache):
    cache_content: dict[str, str] = {}

    def get_message_type(self, battle_event: BattleEvent) -> str:
        existing_checksum = self.cache_content.get(battle_event.id)
        if existing_checksum is None:
            return KafkaMessageType.NewBattle
        return KafkaMessageType.BattleUpdate

    def save_checksum_with_id(self, battle_event: BattleEvent) -> None:
        self.cache_content[battle_event.id] = battle_event.checksum


class OfflineWikidataSource(WikidataSource):
    def __init__(self, battle_events: list[BattleEvent]) -> None:
        self.battle_events = battle_events

    def fetch_battle_events(
        self,
        date_start: str,
        date_end: str,
        limit: int | None = None,
    ) -> list[BattleEvent]:
        return self.battle_events[:limit]


class OfflineProducer(Producer):
    def __init__(self) -> None:
        self.products: list[dict[str, Any]] = []

    def produce(self, payload: KafkaMessage) -> None:
        self.products.append(payload.__dict__)

    def flush(self) -> None:
        pass  # noqa: WPS420


def test_daemon() -> None:
    battle_events = [
        BattleEvent(
            identifier="a",
            name="",
            date=0,
            location="",
            wikipedia_url_stub="",
            coordinates="",
            outcome="",
            image_url_stub="",
        ),
        BattleEvent(
            identifier="a",
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
    assert producer.products[0]["message_type"] == KafkaMessageType.NewBattle
    assert producer.products[1]["message_type"] == KafkaMessageType.BattleUpdate

    assert producer.products[0]["id"] == producer.products[0]["body"]["id"]
