import logging
from threading import Thread

import typer

from wikidata_producer import WikidataProducerDaemon
from wikidata_producer.interchange import KafkaProducer
from wikidata_producer.interchange import RedisChecksumCache
from wikidata_producer.interchange import WikidataHttpSource

app = typer.Typer()


@app.command()
def run(
    kafka_conn_str: str,
    kafka_topic: str,
    redis_dsn: str,
    sleep_interval: int = 5,
    logging_level: int = logging.INFO,
) -> None:
    logging.basicConfig(level=logging_level)
    logging.info("Using configuration:")
    logging.info(f"  kafka_conn_str: {kafka_conn_str}")
    logging.info(f"  kafka_topic: {kafka_topic}")
    logging.info(f"  redis_dsn: {redis_dsn}")
    logging.info(f"  sleep_interval: {sleep_interval}")
    logging.info(f"  logging_level: {logging_level}")

    daemon = WikidataProducerDaemon(
        producer=KafkaProducer(topic=kafka_topic, conn_str=kafka_conn_str),
        wikidata=WikidataHttpSource(),
        checksum_cache=RedisChecksumCache(dsn=redis_dsn),
        sleep_interval_seconds=sleep_interval,
    )
    main_thread = Thread(target=daemon.run, daemon=True)
    try:
        main_thread.start()
        main_thread.join()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected. Exiting.")
        main_thread.join(timeout=0)
        exit(0)


if __name__ == "__main__":
    app()
