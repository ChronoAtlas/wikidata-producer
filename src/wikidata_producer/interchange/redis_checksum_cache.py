from redis import StrictRedis

from wikidata_producer.interchange.checksum_cache import ChecksumCache
from wikidata_producer.models import *


class RedisChecksumCache(ChecksumCache):
    def __init__(self, redis_dsn: str) -> None:
        self.redis = StrictRedis.from_url(
            url=redis_dsn,
            encoding="utf-8",
            decode_responses=True,
        )

    def get_message_type(self, battle_event: BattleEvent) -> KafkaMessageType:
        existing_checksum = self.redis.get(battle_event.id)
        if existing_checksum is None:
            return KafkaMessageType.NewBattle
        return KafkaMessageType.BattleUpdate

    def save_checksum_with_id(self, battle_event: BattleEvent) -> None:

        self.redis.set(battle_event.id, battle_event.checksum)
