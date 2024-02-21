import abc

from wikidata_producer.models.kafka_message import KafkaMessage


class Producer(abc.ABC):
    def connect(self) -> None:
        return

    @abc.abstractmethod
    def produce(self, payload: KafkaMessage) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def flush(self) -> None:
        raise NotImplementedError()
