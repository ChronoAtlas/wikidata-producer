import logging
import time

from redis import StrictRedis
import redis.exceptions  # noqa: WPS301

from wikidata_producer.interchange.checksum_cache import ChecksumCache
from wikidata_producer.models import BattleEvent
from wikidata_producer.models import KafkaMessageType


class RedisChecksumCache(ChecksumCache):
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.redis: StrictRedis | None = None

    def get_connection(self, force_reconnect: bool = False) -> StrictRedis:
        if self.redis is not None and not force_reconnect:
            return self.redis

        while True:
            try:  # noqa: WPS229
                self.redis = StrictRedis.from_url(
                    url=self.dsn,
                    encoding="utf-8",
                    decode_responses=True,
                )
                # I want whatever the library devs were smoking when they wrote those types
                return self.redis  # type: ignore
            except redis.exceptions.ConnectionError as error:
                logging.error(error)
                logging.error("Unable to connect to redis. Retrying in 3 seconds")
                time.sleep(3)

    def get_message_type(self, battle_event: BattleEvent) -> str | None:
        try:
            existing_checksum = self.get_connection().get(battle_event.id)
        except redis.exceptions.ConnectionError as error:
            logging.error(error)
            logging.error("Redis connection lost in produce. Reconnnecting.")
            self.get_connection(force_reconnect=True)
            return None
        if existing_checksum is None:
            return KafkaMessageType.NewBattle
        return KafkaMessageType.BattleUpdate

    def save_checksum_with_id(self, battle_event: BattleEvent) -> None:
        try:
            self.get_connection().set(battle_event.id, battle_event.checksum)
        except redis.exceptions.ConnectionError as error:
            logging.error(error)
            logging.error("Redis connection lost in produce. Reconnnecting.")
            self.get_connection(force_reconnect=True)
