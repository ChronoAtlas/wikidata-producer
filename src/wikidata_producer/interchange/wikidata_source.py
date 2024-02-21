from abc import ABC
from abc import abstractmethod

from wikidata_producer.models.battle_event import BattleEvent


class WikidataSource(ABC):
    @abstractmethod
    def fetch_battle_events(
        self,
        date_start: str,
        date_end: str,
        limit: int | None = None,
    ) -> list[BattleEvent]:
        raise NotImplementedError()
