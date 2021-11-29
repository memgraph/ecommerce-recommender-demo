<h1 align="center">
 🔍 E-Commerce recommender demo 🔍
</h1>

<p align="center">
  <a href="https://github.com/g-despot/ecommerce-recommender-demo/LICENSE">
    <img src="https://img.shields.io/github/license/memgraph/ecommerce-recommender-demo" alt="license" title="license"/>
  </a>
  <a href="https://github.com/g-despot/ecommerce-recommender-demo">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="build" title="build"/>
  </a>
</p>

<p align="center">
  <a href="https://twitter.com/intent/follow?screen_name=memgraphdb">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Follow @memgraphdb"/>
  </a>
  <a href="https://memgr.ph/join-discord">
    <img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"/>
  </a>
</p>

This is a simple stream setup that uses Memgraph to ingest real-time data from a
simulated online store. Data is streamed via Redpanda and Pulsar.

## Data model

<p align="left">
  <a href="https://github.com/g-despot/ecommerce-model">
    <img src="https://public-assets.memgraph.com/github/ecommerce-recommender-demo/ecommerce-model.png"
         alt="ecommerce-model"
         title="ecommerce-model"
         style="width: 75%"/>
  </a>
</p>

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
