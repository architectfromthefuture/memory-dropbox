# Release Playbook (Story-Driven)

Use this playbook so your git history clearly shows technical progression.

## Recommended milestone tags

- `v0.1`: compose stack + migrations + ingest/list endpoints
- `v0.2`: qdrant semantic retrieval
- `v0.3`: hybrid search + redis cache/queue
- `v0.4`: worker indexing + demo script + evaluation hooks
- `v0.5`: kubernetes skeleton + scaling documentation

## Commit style guidance

Keep commits scoped and narratively meaningful:

1. `bootstrap: docker-first app/worker/services skeleton`
2. `data: add postgres schema and alembic migration`
3. `retrieval: add qdrant semantic + hybrid ranking`
4. `ops: add redis queue worker and health checks`
5. `docs: architecture, roadmap, evaluation, demo story`

### Reliability/ops commit examples

Use explicit messages when changes are workarounds or hardening:

- `fix(compose): reduce fragile dependency gating for qdrant startup`
- `fix(api): correct alembic script location in container`
- `fix(startup): add dependency wait-before-migrate guard`
- `docs(ops): record local networking workaround and verification steps`

## Demo checklist before each tag

1. `docker compose up --build`
2. open `/docs` and execute one ingest + one search endpoint
3. run `python scripts/demo.py`
4. verify `/health` services status
5. update milestone notes in `README.md`
6. append any runtime workaround notes to `docs/IMPLEMENTATION_NOTES.md`

