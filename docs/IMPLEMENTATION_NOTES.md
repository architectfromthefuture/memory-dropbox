# Implementation Notes

This file records practical update decisions made during the first local deployment cycle.

## Why this exists

The repository is intended to show progression. These notes make the operational journey explicit so reviewers can see not just the final architecture, but how reliability issues were diagnosed and fixed.

## Timeline of notable updates

1. **Initial compose bootstrap**
   - Added API/worker + Postgres/Redis/Qdrant stack.
   - Added Alembic migrations on API startup.

2. **Qdrant healthcheck adjustment**
   - Early healthcheck behavior could gate startup unexpectedly.
   - Shifted to less fragile dependency semantics for local bring-up.

3. **Alembic path fix**
   - Corrected migration script path for container runtime.

4. **Service readiness guard**
   - Added `apps/api/app/wait_for_services.py`.
   - API now waits for dependency TCP readiness before running migrations.

5. **Host connectivity troubleshooting**
   - Investigated host-to-container reset behavior on `:8000`.
   - Added explicit notes for using `127.0.0.1` when `localhost` behavior is inconsistent.

6. **Compose networking (current)**
   - API uses the default Docker bridge and connects to Postgres/Redis/Qdrant via Compose service names (not `network_mode: host`), for portability across Docker Desktop and Linux.

## Current expected startup path

1. `docker compose up --build -d`
2. API waits for Postgres/Redis/Qdrant.
3. Alembic migration runs.
4. Uvicorn starts serving on `:8000`.

## Reviewer takeaway

The codebase is intentionally modular, but it also contains practical reliability hardening from real local runtime debugging, which is relevant for production-minded engineering roles.

