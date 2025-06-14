from os import path
from fastapi import FastAPI, UploadFile, File, Form
from celery.result import AsyncResult
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware


from tasks import convert_file
from utils.file_ops import save_temp_file
from utils.redis_ops import get_result_path
from celery_worker import celery_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.post('/convert')
async def convert_file(
    file: UploadFile = File(...),
    output_format: str = Form(...),
):
    """
    convert the file into required datatype
    """
    input_path = await save_temp_file(file)
    task = convert_file.delay(input_path, output_format)
    return JSONResponse(
        content={
            'task_id': task.id,
        },
        status_code=202,
    )


@app.get('/status/{task_id}')
async def get_status(task_id: str):
    """
    Check the status of the conversion.
    """
    result = AsyncResult(task_id, app=celery_app)
    return JSONResponse({"status": result.status})


@app.get('/download/{task_id}')
async def download_file(task_id: str):
    """
    Download the converted file based on the task ID.
    """
    file_path = await get_result_path(task_id)

    if not file_path or not file_path.exists(file_path):
        return JSONResponse(
            content={"error": "File not found"},
            status_code=404,
        )
    return FileResponse(file_path, filename=path.basename(file_path), media_type="application/octet-stream")
