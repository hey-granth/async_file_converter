from celery_worker import celery_app
from utils.redis_ops import store_result_path
from os import path, makedirs
import uuid
from config import TEMP_DIR

from converters import get_converter


@celery_app.task(bind=True)
def convert_file(self, input_path: str, output_format: str):
    """
    convert the file into required datatype
    """

    input_ext = path.splitext(input_path)[1].lower()[1:]
    converter = get_converter(input_ext, output_format.lower())

    if not converter:
        raise ValueError(f"Unsupported conversion: {input_ext} to {output_format}")

    output_filename = f"{path.splitext(path.basename(input_path))[0]}_{uuid.uuid4().hex}.{output_format.lower()}"
    makedirs(TEMP_DIR, exist_ok=True)
    output_path = path.join(TEMP_DIR, output_filename)

    converter(input_path, output_path)

    store_result_path(self.request.id, output_path, ttl_seconds=600)

    return output_path
