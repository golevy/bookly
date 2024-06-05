from fastapi import APIRouter, Header, status
from typing import Optional
from src.demo.constants import (
    HEADER_ACCEPT,
    HEADER_CONTENT_TYPE,
    HEADER_USER_AGENT,
    HEADER_HOST,
)


demo_router = APIRouter()


@demo_router.get("/")
async def read_root():
    return {"message": "Hello World"}


@demo_router.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}


@demo_router.get("/get_headers", status_code=status.HTTP_200_OK)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {}
    request_headers[HEADER_ACCEPT] = accept
    request_headers[HEADER_CONTENT_TYPE] = content_type
    request_headers[HEADER_USER_AGENT] = user_agent
    request_headers[HEADER_HOST] = host

    return request_headers
