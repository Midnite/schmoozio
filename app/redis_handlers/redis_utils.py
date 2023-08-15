import aioredis
from .redis_config import REDIS_URL


async def get_redis_connection():
    redis = await aioredis.from_url(REDIS_URL)
    return redis


async def publish_to_redis_channel(channel: str, message: str):
    redis = await get_redis_connection()
    await redis.publish(channel, message)
    redis.close()
    await redis.wait_closed()
