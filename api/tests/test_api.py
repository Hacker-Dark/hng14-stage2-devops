from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_job():
    with patch("api.main.r") as mock_redis:
        mock_redis.lpush = MagicMock()
        mock_redis.hset = MagicMock()

        response = client.post("/jobs")

        assert response.status_code == 200
        assert "job_id" in response.json()


def test_get_job_completed():
    with patch("api.main.r") as mock_redis:
        mock_redis.hget = MagicMock(return_value=b"completed")

        response = client.get("/jobs/test-id")

        assert response.status_code == 200
        assert response.json()["status"] == "completed"


def test_get_job_not_found():
    with patch("api.main.r") as mock_redis:
        mock_redis.hget = MagicMock(return_value=None)

        response = client.get("/jobs/unknown")

        assert response.status_code == 404