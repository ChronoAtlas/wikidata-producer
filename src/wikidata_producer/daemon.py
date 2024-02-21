import json
import logging
import time

from wikidata_producer.interchange import *
from wikidata_producer.models import *


class WikidataProducerDaemon:
    def __init__(
        self,
        producer: Producer,
        wikidata: WikidataSource,
        checksum_cache: ChecksumCache,
        sleep_interval_seconds: int,
        batch_size: int = 5,
    ) -> None:
        self.producer: Producer = producer
        self.wikidata: WikidataSource = wikidata
        self.checksum_cache: ChecksumCache = checksum_cache
        self.sleep_interval_seconds = sleep_interval_seconds
        self.batch_size = batch_size

    def serialize_value(self, queue_item) -> bytes:
        return json.dumps(queue_item).encode("utf-8")

    def run(self) -> None:
        self.producer.connect()
        while True:
            self.tick()
            time.sleep(self.sleep_interval_seconds)

    def tick(self) -> None:
        logging.info("Fetching battle events")
        battle_events = self.wikidata.get_battle_events(
            limit=self.batch_size,
            date_end="",
            date_start="",
        )
        logging.info(f"Processing {len(battle_events)} battle events")
        for battle_event in battle_events:
            message_type = self.checksum_cache.get_message_type(battle_event)
            if message_type is None:
                logging.warning("Skipping message due to connection error")
                continue
            message = KafkaMessage(content=battle_event, message_type=message_type)
            logging.info(f"Sent battle event {battle_event.name} to queue")
            self.producer.produce(payload=message)
            self.checksum_cache.save_checksum_with_id(battle_event=battle_event)
        self.producer.flush()
