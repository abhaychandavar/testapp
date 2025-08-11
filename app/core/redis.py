from typing import Optional, Any
import json
from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create a connection pool
redis_pool = ConnectionPool.from_url(
    settings.redis_url,
    decode_responses=True,  # Automatically decode responses to str instead of bytes
    max_connections=10  # Adjust based on your needs
)

async def get_redis_client() -> Redis:
    """Get a Redis client instance from the connection pool."""
    return Redis(connection_pool=redis_pool)

class RedisClient:
    """Utility class for Redis operations."""
    
    async def __init__(self):
        """Initialize async Redis client."""
        self.client = await get_redis_client()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis."""
        try:
            value = await self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None
    ) -> bool:
        """Set a value in Redis with optional expiration."""
        try:
            serialized_value = json.dumps(value)
            return await self.client.set(
                key,
                serialized_value,
                ex=expire_seconds
            )
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        try:
            return bool(await self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        try:
            return bool(await self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking existence of key {key} in Redis: {str(e)}")
            return False
    
    async def increment(self, key: str) -> Optional[int]:
        """Increment a counter in Redis."""
        try:
            return await self.client.incr(key)
        except Exception as e:
            logger.error(f"Error incrementing key {key} in Redis: {str(e)}")
            return None
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for a key."""
        try:
            return bool(self.client.expire(key, seconds))
        except Exception as e:
            logger.error(f"Error setting expiration for key {key} in Redis: {str(e)}")
            return False
