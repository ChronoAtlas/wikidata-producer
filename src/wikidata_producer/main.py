# import sqlite3
import time

import requests
import typer

from wikidata_producer.models import BattleEvent

app = typer.Typer()

wikidata_query = """
SELECT ?battle ?battleLabel ?date ?locationLabel ?coordinates ?outcomeLabel ?wikipediaLink ?image WHERE {
  ?battle wdt:P31 wd:Q178561;
          wdt:P585 ?date;
          wdt:P276 ?location.
  ?wikipediaLink schema:about ?battle;
                 schema:inLanguage "en";
                 schema:isPartOf <https://en.wikipedia.org/>.
  OPTIONAL { ?battle wdt:P625 ?coordinates. }
  OPTIONAL { ?battle wdt:P793 ?outcome. }
  OPTIONAL { ?battle wdt:P18 ?image. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?date LIMIT 1
"""

wikidata_url = "https://query.wikidata.org/sparql"
wikidata_headers = {"Accept": "application/json"}
wikidata_params = {"query": wikidata_query, "format": "json"}


@app.command()
def run(locations_db_url: str, events_db_url: str, interval_seconds: int = 5) -> None:
    # locations_db = sqlite3.connect(locations_db_url)
    # events_db = sqlite3.connect(events_db_url)

    while True:  # noqa: WPS457
        response = requests.get(
            url=wikidata_url,
            headers=wikidata_headers,
            params=wikidata_params,
        )
        if response.ok:
            for raw_event in response.json()["results"]["bindings"]:
                battle_event = BattleEvent(raw_event)
                print(battle_event)
        else:
            print("Error in the SPARQL request")
            print(response.text)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    app()
