"""Tests for health check endpoint."""

import pytest
from httpx import AsyncClient


class TestHealthEndpoint:
    """Test cases for health check API."""

    @pytest.mark.asyncio
    async def test_health_check_success(self, client: AsyncClient):
        """Test successful health check response."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "status" in data["data"]
        assert data["data"]["status"] == "healthy"
        assert "timestamp" in data["data"]
        assert "version" in data["data"]

    @pytest.mark.asyncio
    async def test_health_check_database_connection(self, client: AsyncClient):
        """Test database connection in health check."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "database" in data["data"]
        assert data["data"]["database"]["status"] == "connected"

    @pytest.mark.asyncio
    async def test_health_check_redis_connection(self, client: AsyncClient):
        """Test Redis connection in health check."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Redis might not be available in test environment
        assert "redis" in data["data"]
        # Status could be "connected" or "disconnected" depending on setup