import redis
from app.core.config import settings

def create_redis_pool():
    return redis.ConnectionPool(
        host = settings.REDIS_URL,
        db = 0,
        decode_responses = True
    )

pool = create_redis_pool()

def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=pool)