import logging
from typing import Any

import requests

from wikidata_producer.interchange.query import WikidataQuery
from wikidata_producer.interchange.wikidata_source import WikidataSource
from wikidata_producer.models.battle_event import BattleEvent


class WikidataHttpSource(WikidataSource):
    def __init__(self) -> None:
        self.url: str = "https://query.wikidata.org/sparql"

    def execute_sparql_query(self, query: str) -> list[dict[str, Any]]:
        params = {  # noqa: WPS110
            "query": query,
            "format": "json",
        }
        headers = {"Accept": "application/json"}
        response = requests.get(
            self.url,
            headers=headers,
            params=params,
            timeout=5000,  # noqa: WPS432
        )
        if response.ok:
            return response.json()["results"]["bindings"]
        logging.error(f"HTTP {response.status_code} on {self.url}")
        return []

    def fetch_battle_events(
        self,
        date_start: str,
        date_end: str,
        limit: int | None = None,
    ) -> list[BattleEvent]:
        query = WikidataQuery.BattlesByDate(limit=limit)
        raw_events = self.execute_sparql_query(query)
        return [
            BattleEvent.from_wikidata_dict(wikidata_entry=raw_event)
            for raw_event in raw_events
        ]
