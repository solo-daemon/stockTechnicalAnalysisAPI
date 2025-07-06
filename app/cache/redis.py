import redis.asyncio as redis
from functools import lru_cache

class RedisCache:
    def __init__(self, url: str = "redis://localhost:6379"):
        self.url = url
        self._client = None

    async def connect(self):
        if self._client is None:
            self._client = redis.from_url(self.url, decode_responses=True)
        return self._client

    async def get_client(self):
        return await self.connect()

# LRU cache ensures singleton behavior
@lru_cache
def get_redis_cache() -> RedisCache:
    return RedisCache()