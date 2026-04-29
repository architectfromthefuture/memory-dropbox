# Architecture

Memory Dropbox is a Docker-first memory substrate: ingest paths persist to PostgreSQL, indexing runs asynchronously via Redis and the worker, and retrieval combines keyword and vector search.

## Data flow

1. Client sends raw text/file to ingestion API.
2. API persists canonical item data in PostgreSQL.
3. API creates index job and pushes queue message to Redis.
4. Worker consumes job, builds embeddings, upserts vectors in Qdrant.
5. Search APIs combine Postgres FTS and Qdrant similarity for hybrid results.

## Module boundaries

- API layer: `apps/api/app/routes/*`
- Domain/data logic: `packages/memory_dropbox/repositories/*`
- Search orchestration: `packages/memory_dropbox/search/hybrid.py`
- Vector integration: `packages/memory_dropbox/vector/*`
- Queue and jobs: `packages/memory_dropbox/queue/*`, `apps/worker/worker/main.py`

## Scale posture

- API horizontal scale: stateless FastAPI replicas.
- Worker horizontal scale: N workers consuming Redis queue.
- Qdrant scale: collection sharding / replica strategy per deployment.
- Postgres scale: managed service and read replicas later.

