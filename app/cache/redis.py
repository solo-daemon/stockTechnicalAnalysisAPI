import redis.asyncio as redis
from functools import lru_cache
from redis.asyncio.connection import ConnectionPool

class RedisCache:
    def __init__(self, url: str = "redis://localhost:6379"):
        self.url = url
        self._pool = ConnectionPool.from_url(self.url, decode_responses=True)
        self._client = redis.Redis(connection_pool=self._pool)

    async def get_client(self):
        return self._client  # pool-backed client

# LRU cache ensures singleton behavior
@lru_cache
def get_redis_cache() -> RedisCache:
    return RedisCache()