import hashlib
from typing import Optional

import flexidate


class BattleEvent:
    def __init__(self, wikidata_entry: dict[str, dict[str, str]]) -> None:
        self.id: str = wikidata_entry["battle"]["value"]
        self.name: str = wikidata_entry["battleLabel"]["value"]
        self.date: float = flexidate.parse(wikidata_entry["date"]["value"]).as_float()
        self.location: str = wikidata_entry["locationLabel"]["value"]
        self.wikipedia_url_stub: str = wikidata_entry["wikipediaLink"]["value"].replace(
            "https://en.wikipedia.org/wiki/",
            "",
        )
        self.coordinates: Optional[str] = (
            wikidata_entry["coordinates"]["value"]
            if "coordinates" in wikidata_entry
            else None
        )
        self.outcome: Optional[str] = (
            wikidata_entry["outcomeLabel"]["value"]
            if "outcomeLabel" in wikidata_entry
            else None
        )
        self.image_url_stub: Optional[str] = (
            wikidata_entry["image"]["value"].replace(
                "http://commons.wikimedia.org/wiki/Special:FilePath/", ""
            )
            if "image" in wikidata_entry
            else None
        )
        # Always keep this last - and make sure it always uses all attributes.
        self.checksum: str = self.generate_checksum()

    def generate_checksum(self) -> str:
        sorted_attributes = sorted(self.__dict__.items())
        concatenated_attributes = "".join(value for _, value in sorted_attributes)
        hash_object = hashlib.sha256(concatenated_attributes.encode())
        return hash_object.hexdigest()
