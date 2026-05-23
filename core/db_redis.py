import os
from redis import Redis


_redis: Redis or  None = None


def get_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis(
            host=os.environ['REDIS_HOST'],
            port=int(os.environ['REDIS_PORT']),
            db=int(os.environ['REDIS_DB']),
            decode_responses=True
        )

    return _redis
