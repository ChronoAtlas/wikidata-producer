# Wikidata-Producer

Wikidata-Producer is a Python application that fetches data from the Wikidata service about historical battles and produces Kafka messages containing this data. Its main use is to provide a way to extract and transmit detailed information about historical battles in a distributed systems context, particularly for real-time data processing and analytics. It uses the Wikidata SPARQL endpoint to run custom queries and transmit the response data as Kafka messages.
Background

The application is written in Python, and it makes use of the Apache Kafka platform for real-time data streaming. Data is fetched from the Wikidata service, a free and open knowledge base that can be read and edited by both humans and machines.

Wikidata provides a SPARQL endpoint for complex queries over its data. The application makes use of this endpoint to obtain detailed information about historical battles (such as the battle name, date, and location, among other details).
Prerequisites

* Python 3.9 or higher
* GNU Make (if you want to use the make targets)
* Docker (if you want to develop or test against a local Kafka cluster)
