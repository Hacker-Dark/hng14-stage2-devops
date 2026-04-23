from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import MagicMock, patch

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}


def test_create_job():
    with patch("api.main.r") as mock_redis:
        mock_redis.lpush = MagicMock()
        mock_redis.hset = MagicMock()

        res = client.post("/jobs")

        assert res.status_code == 200
        assert "job_id" in res.json()


def test_get_job():
    with patch("api.main.r") as mock_redis:
        mock_redis.hget = MagicMock(return_value="completed")

        res = client.get("/jobs/test123")

        assert res.status_code == 200
        assert res.json()["status"] == "completed"


def test_get_job_not_found():
    with patch("api.main.r") as mock_redis:
        mock_redis.hget = MagicMock(return_value=None)

        res = client.get("/jobs/test123")

        assert res.status_code == 404