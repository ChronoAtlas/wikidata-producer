import hashlib
from typing import Any, Optional

import flexidate

from wikidata_producer.models.json_serializable import JsonSerializable


class BattleEvent(JsonSerializable):  # noqa: WPS230
    def __init__(
        self,
        id: str,
        name: str,
        date: float,
        location: str,
        wikipedia_url_stub: str,
        coordinates: str,
        outcome: str,
        image_url_stub: str,
    ) -> None:
        self.id = id
        self.name = name
        self.date = date
        self.location = location
        self.wikipedia_url_stub = wikipedia_url_stub
        self.coordinates = coordinates
        self.outcome = outcome
        self.image_url_stub = image_url_stub
        self.checksum: str = self.generate_checksum()

    @classmethod
    def from_wikidata_dict(cls, wikidata_entry: dict[str, dict[str, str]]) -> None:
        id: str = wikidata_entry["battle"]["value"].split("/")[-1]
        name: str = wikidata_entry["battleLabel"]["value"]
        date: float = flexidate.parse(wikidata_entry["date"]["value"]).as_float()
        location: str = wikidata_entry["locationLabel"]["value"]
        wikipedia_url_stub: str = wikidata_entry["wikipediaLink"]["value"].replace(
            "https://en.wikipedia.org/wiki/",
            "",
        )
        coordinates: Optional[str] = (
            wikidata_entry["coordinates"]["value"]
            if "coordinates" in wikidata_entry
            else None
        )
        outcome: Optional[str] = (
            wikidata_entry["outcomeLabel"]["value"]
            if "outcomeLabel" in wikidata_entry
            else None
        )
        image_url_stub: Optional[str] = (
            wikidata_entry["image"]["value"].replace(
                "http://commons.wikimedia.org/wiki/Special:FilePath/",
                "",
            )
            if "image" in wikidata_entry
            else None
        )
        return cls(
            id=id,
            name=name,
            date=date,
            location=location,
            coordinates=coordinates,
            wikipedia_url_stub=wikipedia_url_stub,
            outcome=outcome,
            image_url_stub=image_url_stub,
        )

    def json(self) -> dict[str, Any]:
        return self.__dict__

    def generate_checksum(self) -> str:
        str_repr = ""
        sorted_obj_keys = sorted(self.__dict__.keys())
        for key in sorted_obj_keys:
            str_repr += f"{key}:{self.__dict__[key]}"
        hash_object = hashlib.sha256(str_repr.encode())
        return hash_object.hexdigest()
