import redis
from redis.exceptions import ConnectionError
from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


def safe_redis_get(key: str):
    try:
        return redis_client.get(key)
    except ConnectionError:
        return None


def safe_redis_set(key: str, value: str, ttl: int = 60):
    try:
        redis_client.setex(key, ttl, value)
    except ConnectionError:
        pass
