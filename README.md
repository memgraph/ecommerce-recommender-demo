# E-Commerce recommender demo

This is a simple stream setup that uses Memgraph to ingest real-time data from a
simulated online store. Data is streamed via Redpanda and Pulsar.

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

```cypher
CREATE PULSAR STREAM views
TOPICS views
TRANSFORM ecommerce.view
SERVICE_URL "pulsar://pulsar:6650";
```

**2.** Another stream is needed to consume product review:

```cypher
CREATE KAFKA STREAM ratings
TOPICS ratings
TRANSFORM ecommerce.rating
BOOTSTRAP_SERVERS "redpanda:29092";
```

**3.** Now, we can start the streams:

```cypher
START ALL STREAMS;
```

**4.** Check if the streams are running correctly:

```cypher
SHOW STREAMS;
```

### Generating recommendations

You can generate a product recommendation by running:

```cypher
MATCH (u:User {id: "1"})-[r:RATED]-(p:Product)
      -[other_r:RATED]-(other:User)
WITH other.id AS other_id,
     avg(r.rating-other_r.rating) AS similarity,
     count(*) AS similar_user_count,
     u.id AS user
ORDER BY similarity
LIMIT 10
WITH collect(other_id) AS similar_user_set, user
MATCH (some_product: Product)-[fellow_rate:RATED]-(fellow_user:User)
WHERE fellow_user.id IN similar_user_set
WITH some_product, avg(fellow_rate.rating) AS prediction_score, user
RETURN some_product.name AS Name, prediction_score, user
ORDER BY prediction_score DESC;
```
