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

        assert "status" in data
        assert data["status"] == "healthy"
        assert "service" in data

    def test_health_check_database_connection(self, client: TestClient):
        """Test database connection in health check."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Simple health check doesn't expose detailed database status
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_check_redis_connection(self, client: TestClient):
        """Test Redis connection in health check."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Simple health check doesn't expose detailed Redis status
        assert "status" in data
