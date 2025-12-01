from redis import Redis
from redis.asyncio import Redis as AsyncRedis

import blanket.io.env as env

BLANKET_REDIS_HOST = env.getenv("BLANKET_REDIS_HOST")
BLANKET_REDIS_PORT = env.getenv("BLANKET_REDIS_PORT")
BLANKET_REDIS_DB = env.getenv("BLANKET_REDIS_DB")


_REDIS_CLIENT: Redis | None = None
_ASYNC_REDIS_CLIENT: AsyncRedis | None = None


def validate_redis_config() -> None:
    if any(
        [
            not BLANKET_REDIS_HOST,
            not BLANKET_REDIS_PORT,
            not BLANKET_REDIS_DB,
        ]
    ):
        raise ValueError(
            "BLANKET_REDIS_HOST, BLANKET_REDIS_PORT, and BLANKET_REDIS_DB must be set"
        )


def get_redis_url() -> str:
    validate_redis_config()
    return f"redis://{BLANKET_REDIS_HOST}:{BLANKET_REDIS_PORT}/{BLANKET_REDIS_DB}"


def get_redis() -> Redis:
    validate_redis_config()
    global _REDIS_CLIENT
    if _REDIS_CLIENT is None:
        _REDIS_CLIENT = Redis(
            host=BLANKET_REDIS_HOST,
            port=BLANKET_REDIS_PORT,
            db=BLANKET_REDIS_DB,
        )
    return _REDIS_CLIENT


def get_async_redis() -> AsyncRedis:
    validate_redis_config()
    global _ASYNC_REDIS_CLIENT
    if _ASYNC_REDIS_CLIENT is None:
        _ASYNC_REDIS_CLIENT = AsyncRedis(
            host=BLANKET_REDIS_HOST,
            port=BLANKET_REDIS_PORT,
            db=BLANKET_REDIS_DB,
        )
    return _ASYNC_REDIS_CLIENT
