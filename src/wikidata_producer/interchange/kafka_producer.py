import json
import logging
import time

import kafka
import kafka.errors

from wikidata_producer.interchange.producer import Producer
from wikidata_producer.models.kafka_message import KafkaMessage


class KafkaProducer(Producer):
    def __init__(self, topic: str, conn_str: str, encoding="utf-8") -> None:
        self.topic = topic
        self.conn_str = conn_str
        self.encoding = encoding
        self.kafka: kafka.KafkaProducer | None = None

    def connect(self) -> None:
        self.get_connection()

    def serialize_value(self, queue_item: KafkaMessage) -> bytes:
        return json.dumps(queue_item.json()).encode(self.encoding)

    def get_connection(self, force_reconnect=False) -> kafka.KafkaProducer:
        if self.kafka is not None and not force_reconnect:
            return self.kafka

        while True:
            try:
                self.kafka = kafka.KafkaProducer(
                    bootstrap_servers=self.conn_str,
                    value_serializer=self.serialize_value,
                    client_id=f"wikidata-producer",
                )
                return self.kafka
            except (kafka.errors.KafkaError, BrokenPipeError) as error:
                logging.error(error)
                logging.error(f"Unable to connect to kafka. Retrying in 3 seconds")
                time.sleep(3)

    def produce(self, payload: KafkaMessage) -> None:
        try:
            self.get_connection().send(topic=self.topic, value=payload)
        except kafka.errors.KafkaError as error:
            logging.error(error)
            logging.error("Kafka connection lost in produce. Reconnnecting.")
            self.get_connection(force_reconnect=True)

    def flush(self) -> None:
        try:
            self.get_connection().flush()
        except (kafka.errors.KafkaError, BrokenPipeError) as error:
            logging.error(error)
            logging.error("Kafka connection lost in flush. Reconnnecting.")
            self.get_connection(force_reconnect=True)
