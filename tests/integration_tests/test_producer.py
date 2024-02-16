import logging
import socket
from threading import Thread

from kafka import KafkaConsumer
import pytest
import requests

from wikidata_producer import WikidataProducer
from wikidata_producer import WikidataQuery

logging.basicConfig(level=logging.INFO)

KAFKA_TOPIC = "integration_test"
KAFKA_HOST = "localhost"
KAFKA_PORT = 29092
KAFKA_CONN_STR = f"{KAFKA_HOST}:{KAFKA_PORT}"


def port_has_service(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_handle:
        return socket_handle.connect_ex((host, port)) == 0


@pytest.fixture
def kafka_producer() -> WikidataProducer:
    if not port_has_service(host=KAFKA_HOST, port=KAFKA_PORT):
        raise ConnectionRefusedError("Unable to connect to kafka")
    return WikidataProducer(
        kafka_conn_str=KAFKA_CONN_STR,
        topic=KAFKA_TOPIC,
        wikidata_query=WikidataQuery.OneRandomBattle,
        sleep_interval=0,
    )


@pytest.fixture
def kafka_consumer() -> KafkaConsumer:
    if not port_has_service(host=KAFKA_HOST, port=KAFKA_PORT):
        raise ConnectionRefusedError("Unable to connect to kafka")
    return KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_CONN_STR)


@pytest.fixture
def remove_network(mocker) -> None:
    mocker.patch.object(requests, "get", side_effect=requests.exceptions.HTTPError)


def test_producer(
    kafka_producer: WikidataProducer,
    kafka_consumer: KafkaConsumer,
) -> None:
    main_thread = Thread(target=kafka_producer.run, daemon=True)
    main_thread.start()
    main_thread.join(timeout=15)

    message_found = False
    for _ in kafka_consumer:
        message_found = True
        break
    assert message_found