import abc
from typing import Any

from wikidata_producer.models.battle_event import BattleEvent


class WikidataSource(abc.ABC):
    def get_battle_events(
        self, date_start: str, date_end: str, limit: int | None = None,
    ) -> list[BattleEvent]:
        raise NotImplementedError()
