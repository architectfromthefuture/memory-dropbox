"""Smoke tests for HTTP health (no Docker required)."""

from starlette.testclient import TestClient

from app.main import app


def test_health_returns_services_matrix() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in ("ok", "degraded")
    assert set(body["services"].keys()) == {"postgres", "redis", "qdrant"}
