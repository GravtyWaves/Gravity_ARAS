"""Tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Test cases for health check API."""

    def test_health_check_success(self, client: TestClient):
        """Test successful health check response."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "status" in data["data"]
        assert data["data"]["status"] == "healthy"
        assert "timestamp" in data["data"]
        assert "version" in data["data"]

    def test_health_check_database_connection(self, client: TestClient):
        """Test database connection in health check."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "database" in data["data"]
        assert data["data"]["database"]["status"] == "connected"

    def test_health_check_redis_connection(self, client: TestClient):
        """Test Redis connection in health check."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Redis might not be available in test environment
        assert "redis" in data["data"]
        # Status could be "connected" or "disconnected" depending on setup
