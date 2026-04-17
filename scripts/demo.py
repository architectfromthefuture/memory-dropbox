from __future__ import annotations

import json
import time

import httpx


BASE_URL = "http://localhost:8000"


def wait_for_health(timeout_s: int = 90) -> None:
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            res = httpx.get(f"{BASE_URL}/health", timeout=5)
            if res.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError("API not healthy within timeout")


def ingest_samples() -> list[str]:
    samples = [
        {
            "title": "Swarm memory design notes",
            "body": "Designing distributed memory layers for swarm orchestration and hardware contexts.",
            "tags": ["swarm", "memory", "architecture"],
            "kind": "note",
            "metadata": {"source": "demo"},
        },
        {
            "title": "Recruiter portfolio positioning",
            "body": "Repos should tell progression from prototypes to robust deployable systems.",
            "tags": ["portfolio", "career"],
            "kind": "note",
            "metadata": {"source": "demo"},
        },
        {
            "title": "Docker and Kubernetes scale path",
            "body": "Start docker-first, then migrate services into kubernetes with worker autoscaling.",
            "tags": ["docker", "kubernetes", "roadmap"],
            "kind": "note",
            "metadata": {"source": "demo"},
        },
    ]

    ids: list[str] = []
    for payload in samples:
        r = httpx.post(f"{BASE_URL}/ingest/text", json=payload, timeout=15)
        r.raise_for_status()
        ids.append(r.json()["id"])
    return ids


def run_queries() -> None:
    for path in ["/search", "/search/semantic", "/search/hybrid"]:
        r = httpx.get(f"{BASE_URL}{path}", params={"query": "swarm architecture", "limit": 5}, timeout=15)
        r.raise_for_status()
        print(f"\n{path} ->")
        print(json.dumps(r.json(), indent=2)[:1200])


def main() -> None:
    print("Waiting for API health...")
    wait_for_health()
    ids = ingest_samples()
    print(f"Ingested {len(ids)} items.")
    run_queries()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()

