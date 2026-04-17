# Architecture Decisions

## ADR-001: Postgres as source of truth

- **Decision**: store all canonical notes/tags/ingestions/jobs in PostgreSQL.
- **Why**: relational integrity, auditability, and future analytics.

## ADR-002: Qdrant for semantic retrieval

- **Decision**: use Qdrant as dedicated vector store.
- **Why**: clean API, high performance, easy path to distributed setup.

## ADR-003: Redis for queue + cache

- **Decision**: Redis backs both queue and hot-path caching.
- **Why**: simple operations, low latency, and common production pattern.

## ADR-004: Docker-first runtime

- **Decision**: first-class local runtime is Docker Compose.
- **Why**: removes machine drift and makes demo/recruiter reproducibility strong.

## ADR-005: Startup reliability guard for local dependencies

- **Decision**: gate API startup behind explicit dependency TCP readiness checks before migration.
- **Why**: health status alone can still race with early connection availability; explicit waiting improves first-run stability.

