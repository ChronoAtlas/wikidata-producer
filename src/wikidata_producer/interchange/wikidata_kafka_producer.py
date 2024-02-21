import json
import logging
import time

from kafka import KafkaProducer
from kafka.errors import KafkaConnectionError
from kafka.errors import NoBrokersAvailable

from wikidata_producer.interchange import *
from wikidata_producer.models import *


class WikidataKafkaProducer(Producer):
    def __init__(self, topic: str, connection_str: str) -> None:
        self.topic = topic
        self.connection_str = connection_str
        self.connection: KafkaProducer | None = None

    def serialize_value(self, value: dict) -> str:
        return json.dumps(value).encode("utf-8")

    def wait_for_connection(self) -> KafkaProducer:
        while True:
            try:
                return KafkaProducer(
                    bootstrap_servers=self.connection_str,
                    value_serializer=self.serialize_value,
                    client_id=f"wikidata-producer",
                )
            except (KafkaConnectionError, NoBrokersAvailable, ValueError) as error:
                logging.warn(error)
                logging.warn(f"No conneciton to kafka. Retrying.")
                time.sleep(5)

    def produce(self, payload: KafkaMessage) -> None:
        self.connection = self.connection or self.wait_for_connection()
        self.connection.send(topic=self.topic, value=payload.json())

    def flush(self) -> None:
        self.connection = self.connection or self.wait_for_connection()
        self.connection.flush()
