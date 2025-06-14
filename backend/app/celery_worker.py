from celery import Celery
from config import REDIS_BROKER_URL, REDIS_RESULT_BACKEND


celery_app = Celery('file_converter', broker=REDIS_BROKER_URL, backend=REDIS_RESULT_BACKEND)

# route all the tasks to one queue
celery_app.conf.task_routes = {
    'app.tasks.*': {'queue': 'file_converter_queue'}
}

# autodiscover tasks in the 'app.tasks' module
celery_app.autodiscover_tasks(['app.tasks'])