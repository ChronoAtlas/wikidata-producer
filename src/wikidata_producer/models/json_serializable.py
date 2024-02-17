import abc
from typing import Any


class JsonSerializable(abc.ABC):

    @abc.abstractmethod
    def json(self) -> dict[str, Any]:
        raise NotImplementedError()
