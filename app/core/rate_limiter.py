"""
Rate Limiting Middleware
Redis-based rate limiting for API endpoints

Built by Elite Team - Backend Security Engineer
"""

import time
from typing import Optional

from fastapi import HTTPException, Request, status
from redis import Redis

from app.core.redis_client import get_redis


class RateLimiter:
    """Redis-based rate limiter."""

    def __init__(
        self,
        redis: Optional[Redis] = None,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
    ):
        """
        Initialize rate limiter.

        Args:
            redis: Redis client instance
            requests_per_minute: Maximum requests per minute per client
            requests_per_hour: Maximum requests per hour per client
        """
        self.redis = redis or get_redis()
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour

    def _get_client_identifier(self, request: Request) -> str:
        """
        Get unique identifier for client.

        Uses IP address and optional API key.
        """
        client_ip = request.client.host if request.client else "unknown"
        api_key = request.headers.get("X-API-Key", "")
        return f"{client_ip}:{api_key}" if api_key else client_ip

    def _get_rate_limit_key(self, identifier: str, window: str) -> str:
        """Generate Redis key for rate limiting."""
        return f"rate_limit:{identifier}:{window}"

    async def check_rate_limit(self, request: Request) -> None:
        """
        Check if request exceeds rate limits.

        Raises HTTPException if limit exceeded.
        """
        if not self.redis:
            return  # Skip rate limiting if Redis not available

        identifier = self._get_client_identifier(request)
        current_time = int(time.time())

        # Check per-minute limit
        minute_key = self._get_rate_limit_key(identifier, f"minute:{current_time // 60}")
        minute_count = self.redis.incr(minute_key)
        if minute_count == 1:
            self.redis.expire(minute_key, 60)  # Expire after 60 seconds

        if minute_count > self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.requests_per_minute} requests per minute",
                headers={"Retry-After": "60"},
            )

        # Check per-hour limit
        hour_key = self._get_rate_limit_key(identifier, f"hour:{current_time // 3600}")
        hour_count = self.redis.incr(hour_key)
        if hour_count == 1:
            self.redis.expire(hour_key, 3600)  # Expire after 1 hour

        if hour_count > self.requests_per_hour:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.requests_per_hour} requests per hour",
                headers={"Retry-After": "3600"},
            )

        # Add rate limit info to response headers
        request.state.rate_limit_remaining_minute = self.requests_per_minute - minute_count
        request.state.rate_limit_remaining_hour = self.requests_per_hour - hour_count


class EndpointRateLimiter:
    """Rate limiter for specific endpoints."""

    def __init__(self, requests: int = 10, window: int = 60):
        """
        Initialize endpoint-specific rate limiter.

        Args:
            requests: Maximum requests allowed
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.redis = get_redis()

    async def __call__(self, request: Request) -> None:
        """Check endpoint-specific rate limit."""
        if not self.redis:
            return

        identifier = f"{request.client.host}:{request.url.path}"
        current_time = int(time.time())
        window_key = f"endpoint_limit:{identifier}:{current_time // self.window}"

        count = self.redis.incr(window_key)
        if count == 1:
            self.redis.expire(window_key, self.window)

        if count > self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Endpoint rate limit exceeded: {self.requests} requests per {self.window}s",
                headers={"Retry-After": str(self.window)},
            )


# Pre-configured rate limiters for different endpoint types
strict_rate_limit = EndpointRateLimiter(requests=10, window=60)  # 10 req/min
moderate_rate_limit = EndpointRateLimiter(requests=30, window=60)  # 30 req/min
relaxed_rate_limit = EndpointRateLimiter(requests=100, window=60)  # 100 req/min
