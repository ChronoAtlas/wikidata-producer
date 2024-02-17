import logging

from kafka import KafkaConsumer
from kafka.errors import KafkaConnectionError
from kafka.errors import NoBrokersAvailable
import pytest
import time

from wikidata_producer import *
from wikidata_producer.interchange import *

logging.basicConfig(level=logging.DEBUG)

KAFKA_TOPIC = "integration_test"
KAFKA_HOST = "localhost"
KAFKA_PORT = 29092
KAFKA_CONN_STR = f"{KAFKA_HOST}:{KAFKA_PORT}"
REDIS_DSN = "redis://localhost:6379"
BATCH_SIZE=5


@pytest.fixture
def daemon() -> WikidataProducerDaemon:
    return WikidataProducerDaemon(
        producer=WikidataKafkaProducer(topic=KAFKA_TOPIC, connection_str=KAFKA_CONN_STR),
        wikidata=WikidataHttpSource(),
        checksum_cache=RedisChecksumCache(redis_dsn=REDIS_DSN),
        sleep_interval_seconds=0,
        batch_size=BATCH_SIZE,
    )


@pytest.fixture
def kafka_consumer() -> KafkaConsumer:
    tries = 0
    while tries < 10:
        try:
            return KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_CONN_STR)
        except (KafkaConnectionError, NoBrokersAvailable, ValueError) as error:
            logging.warn(f"No conneciton to kafka from consumer. Retrying.")
            tries += 1
            time.sleep(1)
    raise TimeoutError()


def test_daemon(
    daemon: WikidataProducerDaemon,
    kafka_consumer: KafkaConsumer,
) -> None:
    daemon.tick()

    message_found = False
    for _ in kafka_consumer.poll(timeout_ms=5000, max_records=BATCH_SIZE):
        message_found = True
        break
    kafka_consumer.close()
    assert message_found
