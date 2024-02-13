CREATE TABLE battle_events (
    id VARCHAR NOT NULL,
    date DATE NOT NULL,
    location VARCHAR NOT NULL,
    wikipedia_url_stub VARCHAR NOT NULL,
    outcome VARCHAR,
    image_link_stub VARCHAR,
    PRIMARY KEY (id)
)
