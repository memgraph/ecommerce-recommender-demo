# E-Commerce recommender

This is a simple stream setup that uses Memgraph to ingest real-time data from a
simulated online store.

## Usage

### Prerequisites

You will need:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/) (included with
  Docker Desktop on Windows and macOS)

### Running the app

**1.** First, remove possibly running containers:

```
docker-compose rm -fs
```

**2.** Build all the needed images:

```
docker-compose build
```

**3.** Start the **Redpanda** and **Apache Pulsar** services:

```
docker-compose up -d core
```

**4.** Start the data stream:

```
docker-compose up stream
```

**5.** Start Memgraph:

```
docker-compose up memgraph-mage
```

### Creating the streams in Memgraph

**1.** First, we will create a stram for consuming product views:

```
CREATE PULSAR STREAM views
TOPICS views
TRANSFORM ecommerce.view
SERVICE_URL "pulsar://pulsar:6650";
```

**2.** Another stream is needed to consume product review:

```
CREATE KAFKA STREAM ratings
TOPICS ratings
TRANSFORM ecommerce.rating
BOOTSTRAP_SERVERS "redpanda:29092";
```

**3.** Now, we can start the streams:

```
START ALL STREAMS;
```

**4.** Check if the streams are running correctly:

```
SHOW STREAMS;
```
