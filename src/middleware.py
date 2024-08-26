from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging


logger = logging.getLogger("uvicorn.access")
logging.disable = True


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} - completed after {processing_time}s"
        print(message)

        return response
