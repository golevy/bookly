from fastapi import FastAPI
from src.books.routes import book_router
from src.demo.routes import demo_router

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(demo_router, prefix=f"/api/{version}/demo", tags=["demo"])
