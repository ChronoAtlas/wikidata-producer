import logging
from threading import Thread

import typer

from wikidata_producer import WikidataProducer
from wikidata_producer import WikidataQuery

app = typer.Typer()


@app.command()
def run(
    kafka_conn_str: str,
    kafka_topic: str,
    sleep_interval: int = 5,
    logging_level: int = logging.INFO,
) -> None:
    logging.basicConfig(level=logging_level)
    producer = WikidataProducer(
        kafka_conn_str=kafka_conn_str,
        topic=kafka_topic,
        wikidata_query=WikidataQuery.BattlesByDate(limit=5),
        sleep_interval=sleep_interval,
    )
    main_thread = Thread(target=producer.run, daemon=True)
    main_thread.start()
    main_thread.join()


if __name__ == "__main__":
    app()
