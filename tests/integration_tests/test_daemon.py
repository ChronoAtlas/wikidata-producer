import logging
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import pytest

from wikidata_producer import WikidataProducerDaemon
from wikidata_producer.interchange import KafkaProducer
from wikidata_producer.interchange import RedisChecksumCache
from wikidata_producer.interchange import WikidataHttpSource

logging.basicConfig(level=logging.DEBUG)

KAFKA_TOPIC = "tests"
KAFKA_HOST = "localhost"
KAFKA_PORT = 29092
KAFKA_CONN_STR = f"{KAFKA_HOST}:{KAFKA_PORT}"
REDIS_DSN = "redis://localhost:6379"
BATCH_SIZE = 5


@pytest.fixture
def daemon() -> WikidataProducerDaemon:
    return WikidataProducerDaemon(
        producer=KafkaProducer(topic=KAFKA_TOPIC, conn_str=KAFKA_CONN_STR),
        wikidata=WikidataHttpSource(),
        checksum_cache=RedisChecksumCache(dsn=REDIS_DSN),
        sleep_interval_seconds=0,
        batch_size=BATCH_SIZE,
    )


@pytest.fixture
def kafka_consumer() -> KafkaConsumer:
    then = time.time()
    now = time.time()
    max_wait_seconds = 15
    while now - then < max_wait_seconds:
        logging.info(
            f"Attempting to create kafka consumer ({int(now - then)}/{max_wait_seconds} seconds)",
        )
        try:
            return KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_CONN_STR,
                auto_offset_reset="earliest",
            )
        except (KafkaError, ValueError) as error:
            logging.warning(error)
            logging.warning("No conneciton to kafka from consumer. Retrying.")
            now = time.time()
            time.sleep(1)
    raise TimeoutError()


def test_daemon(
    daemon: WikidataProducerDaemon,
    kafka_consumer: KafkaConsumer,
) -> None:
    daemon.producer.connect()
    daemon.tick()

    message_found = False
    for _ in kafka_consumer.poll(timeout_ms=5000, max_records=1):
        message_found = True
        break
    kafka_consumer.close()
    assert message_found
