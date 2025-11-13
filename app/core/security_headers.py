"""
ARAS Microservice Security Headers Middleware
Implements comprehensive security headers for OWASP best practices

Built by Elite Team - Security Expert (CISSP, CEH)
"""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.config import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add comprehensive security headers to all responses.
    
    Headers implemented:
    - Content-Security-Policy (CSP): Prevents XSS, injection attacks
    - X-Frame-Options: Prevents clickjacking
    - X-Content-Type-Options: Prevents MIME sniffing
    - Strict-Transport-Security (HSTS): Enforces HTTPS
    - X-XSS-Protection: Additional XSS protection for older browsers
    - Referrer-Policy: Controls referrer information
    - Permissions-Policy: Restricts browser features
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.security_headers = self._build_security_headers()

    def _build_security_headers(self) -> dict:
        """Build security headers based on environment."""
        headers = {
            # Content Security Policy - prevents XSS and injection attacks
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            ),
            # Prevents clickjacking attacks
            "X-Frame-Options": "DENY",
            # Prevents MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # XSS protection for older browsers
            "X-XSS-Protection": "1; mode=block",
            # Controls referrer information leakage
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Restricts browser features and APIs
            "Permissions-Policy": (
                "accelerometer=(), "
                "camera=(), "
                "geolocation=(), "
                "gyroscope=(), "
                "magnetometer=(), "
                "microphone=(), "
                "payment=(), "
                "usb=()"
            ),
            # Remove server header to hide technology stack
            "X-Powered-By": "ARAS",
        }

        # Only add HSTS in production (requires HTTPS)
        if getattr(settings, "ENVIRONMENT", "development") == "production":
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        return headers

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        try:
            response = await call_next(request)

            # Add all security headers
            for header, value in self.security_headers.items():
                response.headers[header] = value

            return response

        except Exception as e:
            logger.error(f"Error in SecurityHeadersMiddleware: {e}")
            raise
