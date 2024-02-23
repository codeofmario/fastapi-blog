from redis import asyncio

from app.config.settings import get_settings

# Get settings
settings = get_settings()


async def get_redis() -> asyncio.Redis:
    return await asyncio.from_url(f"redis://{settings.redis_host}:{settings.redis_port}",
                                  password=settings.redis_password, encoding="utf-8", decode_responses=True)
