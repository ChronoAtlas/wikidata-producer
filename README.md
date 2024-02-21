# Wikidata Producer

This project contains a Kafka producer for battle events which are fetched from WikiData.

## File structure

The project comprises multiple python files grouped into the following directories:

- `src/wikidata_producer`: Main directory containing application logic.
  - `interchange`: Directory implementing producer behavior and wikidata source abstraction.
  - `models`: Directory containing the relevant data models.
  - `main.py`: Entry point to the application
  - `daemon.py`: Defines the main flow of the application
  - `version.py`: Contains the current version of the application.

## Entry point

The application is initialized and run from `main.py`. We utilize Typer, a Python CLI creation package, to build a command-line interface. The `run` command accepts Kafka connection details, Redis DSN, sleep interval and logging level as argument inputs.

## Main Logic

The `WikidataProducerDaemon` starts a daemon thread and runs indefinitely until terminated by the user. On every tick, it fetches batch of battle events from WikiData, prepares messages for each of them and publishes these messages to a Kafka topic via the Producer.

## Producer and Data Source

The `KafkaProducer` is an implementation of a `Producer` interface that connects to a Kafka server and sends messages. Each message payload is an instance of `KafkaMessage` which bundles a BattleEvent with a message type indicating whether it's a new or updated record.

As a data source, the `WikidataHttpSource` queries a SPARQL endpoint to retrieve battle events. The source transforms results from the Wikidata API into `BattleEvents`.

## Checksum Caching

To determine if a battle event is new or updated, we perform checksum caching. `RedisChecksumCache` performs this task by storing a checksum for each event in a Redis server. Using the checksum, it sets the KafkaMessage types as either "NewBattle" or "BattleUpdate".

## Note

Please make sure that your environment supports Kafka and Redis, and have the servers running before starting the application.

## Prerequisites

You need the following installed:

- Python 3.10 or higher.

## Setup

1. Clone the repository.
2. Create a virtual environment `python3 -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install dependencies `pip install -r requirements.txt`
5. Run the application as shown below.

## Running the application

```
wikidata_producer --help

 Usage: wikidata_producer [OPTIONS] KAFKA_CONN_STR KAFKA_TOPIC REDIS_DSN

╭─ Arguments ──────────────────────────────────────────────────────────────╮
│ *    kafka_conn_str      TEXT  [default: None] [required]                │
│ *    kafka_topic         TEXT  [default: None] [required]                │
│ *    redis_dsn           TEXT  [default: None] [required]                │
╰──────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────╮
│ --sleep-interval            INTEGER                [default: 5]          │
│ --logging-level             INTEGER                [default: 20]         │
│ --install-completion        [bash|zsh|fish|powers  Install completion    │
│                             hell|pwsh]             for the specified     │
│                                                    shell.                │
│                                                    [default: None]       │
│ --show-completion           [bash|zsh|fish|powers  Show completion for   │
│                             hell|pwsh]             the specified shell,  │
│                                                    to copy it or         │
│                                                    customize the         │
│                                                    installation.         │
│                                                    [default: None]       │
│ --help                                             Show this message and │
│                                                    exit.                 │
╰──────────────────────────────────────────────────────────────────────────╯
```

## Contributing and feedback

Contributions, feedback, and questions are welcomed. Feel free to submit a pull request or issue.
