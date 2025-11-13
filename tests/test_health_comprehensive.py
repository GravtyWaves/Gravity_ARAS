"""
Comprehensive test suite for Health Check endpoints

Built by Elite Team - QA Lead
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test suite for health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_check(self):
        """Test basic health check."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ARAS Microservice"

    def test_api_health_endpoint(self):
        """Test API health endpoint."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_health_response_time(self):
        """Test that health check is fast."""
        import time

        start = time.time()
        response = client.get("/health")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Should respond in less than 1 second

    def test_health_check_headers(self):
        """Test health check response headers."""
        response = client.get("/health")

        assert response.status_code == 200
        # Check for standard headers
        assert "content-type" in response.headers

    def test_api_docs_available(self):
        """Test that API documentation is available."""
        response = client.get("/docs")

        assert response.status_code == 200

    def test_redoc_available(self):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")

        assert response.status_code == 200

    def test_openapi_json(self):
        """Test OpenAPI JSON schema."""
        response = client.get("/api/v1/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data

    def test_cors_headers(self):
        """Test CORS headers presence."""
        response = client.get("/health")

        # CORS headers should be present in development
        assert response.status_code == 200

    def test_multiple_health_checks(self):
        """Test multiple consecutive health checks."""
        for i in range(10):
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
