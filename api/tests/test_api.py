import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

with patch('redis.Redis'):
    from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that health endpoint returns 200 and correct message"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_job():
    """Test that creating a job returns a job_id"""
    with patch('main.r') as mock_redis:
        mock_redis.lpush = MagicMock()
        mock_redis.hset = MagicMock()
        response = client.post("/jobs")
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert len(data["job_id"]) > 0


def test_get_job_status_completed():
    """Test that getting a job returns its status"""
    with patch('main.r') as mock_redis:
        mock_redis.hget = MagicMock(return_value=b"completed")
        response = client.get("/jobs/fake-job-123")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == "fake-job-123"
        assert data["status"] == "completed"


def test_get_job_not_found():
    """Test that getting a non-existent job returns 404"""
    with patch('main.r') as mock_redis:
        mock_redis.hget = MagicMock(return_value=None)
        response = client.get("/jobs/nonexistent-job")
        assert response.status_code == 404


def test_create_job_calls_redis():
    """Test that creating a job actually pushes to redis queue"""
    with patch('main.r') as mock_redis:
        mock_redis.lpush = MagicMock()
        mock_redis.hset = MagicMock()
        client.post("/jobs")
        assert mock_redis.lpush.called
        assert mock_redis.hset.called

# api/tests/test_api.py
from app import app

def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200

def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200

def test_json():
    client = app.test_client()
    res = client.get("/")
    assert res.is_json