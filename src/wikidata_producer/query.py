from typing import Optional


class WikidataQuery:
    @classmethod
    def BattlesByDate(cls, limit: Optional[int] = None):
        return (
            'SELECT ?battle ?battleLabel ?date ?locationLabel ?coordinates ?outcomeLabel ?wikipediaLink ?image WHERE { ?battle wdt:P31 wd:Q178561; wdt:P585 ?date; wdt:P276 ?location. ?wikipediaLink schema:about ?battle; schema:inLanguage "en"; schema:isPartOf <https://en.wikipedia.org/>. OPTIONAL { ?battle wdt:P625 ?coordinates. } OPTIONAL { ?battle wdt:P793 ?outcome. } OPTIONAL { ?battle wdt:P18 ?image. } SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } } ORDER BY ?date %s'
            % ("" if limit is None else f"LIMIT {limit}")
        )

    @classmethod
    def OneRandomBattle(cls):
        return 'SELECT ?battle ?battleLabel ?date ?locationLabel ?coordinates ?outcomeLabel ?wikipediaLink ?image WHERE { ?battle wdt:P31 wd:Q178561; wdt:P585 ?date; wdt:P276 ?location. ?wikipediaLink schema:about ?battle; schema:inLanguage "en"; schema:isPartOf <https://en.wikipedia.org/>. OPTIONAL { ?battle wdt:P625 ?coordinates. } OPTIONAL { ?battle wdt:P793 ?outcome. } OPTIONAL { ?battle wdt:P18 ?image. } SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } } LIMIT 1'
