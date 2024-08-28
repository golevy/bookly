from fastapi import FastAPI
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging


logger = logging.getLogger("uvicorn.access")
logging.disable = True


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} - completed after {processing_time}s"
        print(message)

        return response

    @app.middleware("http")
    async def authorization(request: Request, call_next):
        if not "Authorization" in request.headers:
            return JSONResponse(
                content={
                    "message": "Authorization header is missing",
                    "resolution": "Please provide a valid token in the Authorization header",
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        response = await call_next(request)

        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
