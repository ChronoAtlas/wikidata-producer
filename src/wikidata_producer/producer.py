import json
import logging
import time

from kafka import KafkaProducer
from kafka.errors import KafkaConnectionError
from kafka.errors import NoBrokersAvailable
import requests

from wikidata_producer.models import BattleEvent


class WikidataProducer:
    instance_count = 0

    def __init__(
        self, kafka_conn_str: str, topic: str, wikidata_query: str, sleep_interval: int
    ) -> None:
        self.topic: str = topic
        self.wikidata_query: str = wikidata_query
        self.sleep_interval: int = sleep_interval
        self.kafka_conn_str: str = kafka_conn_str
        self.kafka_producer: KafkaProducer = self.wait_for_kafka_and_create_producer()

    def wait_for_kafka_and_create_producer(self) -> KafkaProducer:
        while True:
            try:
                WikidataProducer.instance_count += 1
                return KafkaProducer(
                    bootstrap_servers=self.kafka_conn_str,
                    value_serializer=self.serialize_value,
                    client_id=f"wikidata-producer-{WikidataProducer.instance_count}",
                )
            except (KafkaConnectionError, NoBrokersAvailable, ValueError) as error:
                logging.error(error)
                logging.error(
                    f"Unable to connect to kafka. Retrying in {self.sleep_interval} seconds"
                )
                time.sleep(self.sleep_interval)

    def serialize_value(self, queue_item) -> bytes:
        return json.dumps(queue_item).encode("utf-8")

    def extract_battle_events(self, response: requests.Response) -> list[BattleEvent]:
        if not response.ok:
            match response.status_code:
                case 429:
                    logging.warn(
                        f"Wikidata rate limit hit. Waiting {self.sleep_interval} seconds"
                    )
                case _:
                    logging.error(f"HTTP error {response.status_code} from wikidata")
                    logging.error(response.text)
            return []
        raw_dict_response = response.json()["results"]["bindings"]
        return [BattleEvent(raw_event) for raw_event in raw_dict_response]

    def run(self) -> None:
        url = "https://query.wikidata.org/sparql"
        headers = {"Accept": "application/json"}
        params = {"query": self.wikidata_query, "format": "json"}

        while True:
            logging.info("Sending wikidata request")
            response = requests.get(url=url, headers=headers, params=params)
            battle_events = self.extract_battle_events(response=response)
            self.publish_battle_events(battle_events=battle_events)
            time.sleep(self.sleep_interval)

    def publish_battle_events(self, battle_events: list[BattleEvent]) -> None:
        for battle_event in battle_events:
            logging.info(f"Publishing event {battle_event.name}")
            self.kafka_producer.send(topic=self.topic, value=battle_event.__dict__)
        self.kafka_producer.flush()
