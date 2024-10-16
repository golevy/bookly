from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.demo.routes import demo_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.errors import register_all_errors
from src.middleware import register_middleware


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"========================")
    print(f"🚀 Server is starting...")
    await init_db()
    print(f"========================")
    yield
    print(f"========================")
    print(f"🚀 Server has been stopped")
    print(f"========================")


version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to:
- Create, read, update, and delete books.
- Add reviews to books
- Add tags to books etc.
"""

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Bookly",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    contact={
        "name": "Levy Lv",
        "url": "https://github.com/golevy",
        "email": "golvwei@gmail.com",
    },
    terms_of_service="https://github.com/golevy/bookly",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

register_all_errors(app)

register_middleware(app)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(demo_router, prefix=f"/api/{version}/demo", tags=["demo"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
