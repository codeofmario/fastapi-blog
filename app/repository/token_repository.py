from redis.asyncio import Redis
from fastapi import Depends

from app.config.redis import get_redis


class TokenRepository:
    def __init__(self,
                 redis: Redis = Depends(get_redis)):
        self.redis = redis

    async def get(self, key: str) -> str:
        return await self.redis.get(key)

    async def save(self, key: str, token: str, exp: int) -> bool:
        await self.redis.set(key, token, exp)
        return True

    async def delete(self, key: str) -> bool:
        await self.redis.delete(key)
        return True
