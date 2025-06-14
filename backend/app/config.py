from os import getenv
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(getenv('REDIS_PORT', 6379))
REDIS_DB = int(getenv('REDIS_DB', 0))
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

TEMP_DIR = '/tmp/file_converter'

REDIS_BROKER_URL = getenv('REDIS_BROKER_URL')
REDIS_RESULT_BACKEND = getenv('REDIS_RESULT_BACKEND')