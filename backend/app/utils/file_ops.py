# code to save program files temporarily

from aiofiles import open
from os import makedirs, path
from uuid import uuid4
from backend.app.config import TEMP_DIR

# uuid is used to generate unique filenames


makedirs(TEMP_DIR, exist_ok=True)


async def save_temp_file(upload_file) -> str:
    """
    Save the uploaded file to a temporary location and return the file path.
    """
    file_ext = path.splitext(upload_file.filename)[1]
    temp_filename = f"{uuid4().hex}{file_ext}"
    temp_path = path.join(TEMP_DIR, temp_filename)

    async with open(temp_path, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)

    return temp_path
