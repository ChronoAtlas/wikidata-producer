import abc

from redis import StrictRedis

from wikidata_producer.models import *


class ChecksumCache(abc.ABC):
    @abc.abstractmethod
    def get_message_type(self, battle_event: BattleEvent) -> KafkaMessageType:
        raise NotImplementedError()

    @abc.abstractmethod
    def save_checksum_with_id(self, battle_event: BattleEvent) -> None:
        raise NotImplementedError()
