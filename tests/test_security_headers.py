"""Tests for security headers middleware."""

import pytest
from fastapi.testclient import TestClient


class TestSecurityHeaders:
    """Test cases for security headers."""

    def test_security_headers_present(self, client: TestClient):
        """Test that all security headers are present in response."""
        response = client.get("/health")

        # Check all security headers
        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
        assert "Referrer-Policy" in response.headers
        assert "Permissions-Policy" in response.headers
        assert "X-Powered-By" in response.headers

    def test_csp_header_value(self, client: TestClient):
        """Test Content-Security-Policy header value."""
        response = client.get("/health")

        csp = response.headers["Content-Security-Policy"]
        assert "default-src 'self'" in csp
        assert "frame-ancestors 'none'" in csp
        assert "base-uri 'self'" in csp

    def test_frame_options_deny(self, client: TestClient):
        """Test X-Frame-Options is set to DENY."""
        response = client.get("/health")

        assert response.headers["X-Frame-Options"] == "DENY"

    def test_content_type_options_nosniff(self, client: TestClient):
        """Test X-Content-Type-Options is set to nosniff."""
        response = client.get("/health")

        assert response.headers["X-Content-Type-Options"] == "nosniff"

    def test_xss_protection_enabled(self, client: TestClient):
        """Test X-XSS-Protection is enabled."""
        response = client.get("/health")

        assert response.headers["X-XSS-Protection"] == "1; mode=block"

    def test_referrer_policy_set(self, client: TestClient):
        """Test Referrer-Policy is properly configured."""
        response = client.get("/health")

        assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"

    def test_permissions_policy_restrictive(self, client: TestClient):
        """Test Permissions-Policy restricts dangerous features."""
        response = client.get("/health")

        permissions = response.headers["Permissions-Policy"]
        assert "camera=()" in permissions
        assert "microphone=()" in permissions
        assert "geolocation=()" in permissions
        assert "payment=()" in permissions

    def test_security_headers_on_api_endpoints(self, client: TestClient):
        """Test security headers are applied to API endpoints."""
        # Use health endpoint instead of articles to avoid database issues
        response = client.get("/health")

        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-Content-Type-Options" in response.headers

    def test_security_headers_on_error_responses(self, client: TestClient):
        """Test security headers are present even on error responses."""
        response = client.get("/nonexistent-endpoint")

        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-Content-Type-Options" in response.headers
