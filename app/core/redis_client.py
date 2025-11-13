"""
ARAS Microservice Redis Client
Caching and pub/sub functionality

Built by Elite Team - DevOps Engineer (PhD in Distributed Systems)
"""

import json
import logging
from typing import Any, Optional

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis client for caching and messaging."""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            self.client = redis.from_url(settings.REDIS_URL)
            await self.client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            logger.warning("Continuing without Redis caching...")
            self.client = None  # Set to None to allow graceful degradation

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")

    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis."""
        if not self.client:
            return None
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set value in Redis with optional TTL."""
        if not self.client:
            return False
        try:
            ttl = ttl or settings.REDIS_CACHE_TTL
            return await self.client.set(key, value, ex=ttl)
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        if not self.client:
            return False
        try:
            return bool(await self.client.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if not self.client:
            return False
        try:
            return bool(await self.client.exists(key))
        except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
            return False

    async def publish(self, channel: str, message: Any) -> bool:
        """Publish message to Redis channel."""
        if not self.client:
            return False
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            return bool(await self.client.publish(channel, message))
        except Exception as e:
            logger.error(f"Redis PUBLISH error for channel {channel}: {e}")
            return False

    async def set_json(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """Set JSON data in Redis."""
        return await self.set(key, json.dumps(data), ttl)

    async def get_json(self, key: str) -> Optional[Any]:
        """Get JSON data from Redis."""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON for key {key}: {e}")
        return None


# Global Redis client instance
redis_client = RedisClient()


def get_redis() -> Optional[redis.Redis]:
    """Get Redis client instance (for dependency injection)."""
    return redis_client.client if redis_client else None
