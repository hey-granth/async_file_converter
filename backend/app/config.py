from os import getenv

REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(getenv('REDIS_PORT', 6379))
REDIS_DB = int(getenv('REDIS_DB', 0))

TEMP_DIR = '/tmp/file_converter'

REDIS_BROKER_URL = getenv('REDIS_BROKER_URL', 'redis://redis:6379/0')
REDIS_RESULT_BACKEND = getenv('REDIS_RESULT_BACKEND', 'redis://redis:6379/1')