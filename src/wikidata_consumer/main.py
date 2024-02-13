import time

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import typer

from wikidata_consumer.models import Base

app = typer.Typer()

wikidata_query = """
SELECT ?battle ?battleLabel ?date ?coordinates WHERE {
  ?battle wdt:P31/wdt:P279* wd:Q178561; wdt:P585 ?date; wdt:P625 ?coordinates.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?date LIMIT 100
"""
wikidata_url = "https://query.wikidata.org/sparql"
wikidata_headers = {"Accept": "application/json"}
wikidata_params = {"query": wikidata_query, "format": "json"}


@app.command()
def run(locations_db_url: str, events_db_url: str, interval_seconds: int = 5) -> None:

    while True:  # noqa: WPS457
        response = requests.get(
            wikidata_url, headers=wikidata_headers, params=wikidata_params
        )
        if not response.ok:
            print("Error in the SPARQL request")
            print(response.text)
        else:
            data = response.json()
            for item in data["results"]["bindings"]:
                battle = item["battleLabel"]["value"]
                date = item["date"]["value"]
                coordinates = item["coordinates"]["value"]
                print(f"Battle: {battle}, Date: {date}, Coordinates: {coordinates}")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    app()
