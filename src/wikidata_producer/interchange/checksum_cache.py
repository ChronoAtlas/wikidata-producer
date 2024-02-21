import abc

from wikidata_producer.models.battle_event import BattleEvent


class ChecksumCache(abc.ABC):
    @abc.abstractmethod
    def get_message_type(self, battle_event: BattleEvent) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def save_checksum_with_id(self, battle_event: BattleEvent) -> None:
        raise NotImplementedError()
