# to store and retrieve converted file paths from redis

import redis
from backend.app.config import REDIS_HOST, REDIS_PORT, REDIS_DB


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def store_result_path(task_id: str, file_path: str, ttl_seconds: int = 600):
    """
    Store the result file path in Redis with an expiration time.
    """
    redis_client.set(task_id, file_path, ex=ttl_seconds)

def get_result_path(task_id: str) -> str:
    """
    Retrieve the result file path from Redis.
    """
    return redis_client.get(f'result_{task_id}')

