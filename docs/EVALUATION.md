# Retrieval Evaluation

Use this harness approach for research-facing validation:

1. Create a golden query set (`query`, `expected_item_ids`).
2. Run each query against keyword, semantic, and hybrid endpoints.
3. Track:
   - hit@k
   - mrr
   - latency p50/p95
4. Compare by corpus size and ingestion type.

## Baseline recommendation

- 50 hand-curated queries
- k = 5 and 10
- weekly regression checks before milestone tags

