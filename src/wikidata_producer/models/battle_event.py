import hashlib

import flexidate


class BattleEvent:  # noqa: WPS230
    def __init__(  # noqa: WPS211
        self,
        identifier: str,
        name: str,
        date: float,
        location: str,
        wikipedia_url_stub: str,
        coordinates: str | None,
        outcome: str | None,
        image_url_stub: str | None,
    ) -> None:
        self.id = identifier
        self.name = name
        self.date = date
        self.location = location
        self.wikipedia_url_stub = wikipedia_url_stub
        self.coordinates = coordinates
        self.outcome = outcome
        self.image_url_stub = image_url_stub
        self.checksum: str = self.generate_checksum()

    @classmethod
    def from_wikidata_dict(  # noqa: WPS210
        cls,
        wikidata_entry: dict[str, dict[str, str]],
    ) -> "BattleEvent":
        identifier: str = wikidata_entry["battle"]["value"].split("/")[-1]
        name: str = wikidata_entry["battleLabel"]["value"]
        date: float = flexidate.parse(wikidata_entry["date"]["value"]).as_float()
        location: str = wikidata_entry["locationLabel"]["value"]
        wikipedia_url_stub: str = wikidata_entry["wikipediaLink"]["value"].replace(
            "https://en.wikipedia.org/wiki/",
            "",
        )
        coordinates: str | None = (
            wikidata_entry["coordinates"]["value"]
            if "coordinates" in wikidata_entry
            else None
        )
        outcome: str | None = (
            wikidata_entry["outcomeLabel"]["value"]
            if "outcomeLabel" in wikidata_entry
            else None
        )
        image_url_stub: str | None = (
            wikidata_entry["image"]["value"].replace(
                "http://commons.wikimedia.org/wiki/Special:FilePath/",
                "",
            )
            if "image" in wikidata_entry
            else None
        )
        return cls(
            identifier=identifier,
            name=name,
            date=date,
            location=location,
            coordinates=coordinates,
            wikipedia_url_stub=wikipedia_url_stub,
            outcome=outcome,
            image_url_stub=image_url_stub,
        )

    def generate_checksum(self) -> str:
        str_repr = ""
        sorted_obj_keys = sorted(self.__dict__.keys())
        for key in sorted_obj_keys:  # noqa: WPS519 linter has absolutely lost its mind
            str_repr += f"{key}:{self.__dict__[key]}"  # noqa: WPS336
        hash_object = hashlib.sha256(str_repr.encode())
        return hash_object.hexdigest()
