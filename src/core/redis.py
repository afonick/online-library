import redis.asyncio as redis

from src.core.config import settings


class RedisConnector:
    def __init__(self, url):
        self.url = url
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(self.url)

    async def set(self, key, value, expire=None):
        if expire:
            return await self.redis.set(key, value, ex=expire)
        return await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        return await self.redis.delete(key)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()


redis_connector = RedisConnector(url=settings.REDIS_URL)
