from fastapi import FastAPI
from src.books.routers import book_router
from src.auth.routers import auth_router
from src.db.main import get_db
from contextlib import asynccontextmanager



@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is Starting")
    await get_db()
    yield
    print("server is closing")

version="v1"
app=FastAPI(
    version=version
)

app.include_router(book_router,prefix=f"/api/{version}/book",tags=["Book"])
app.include_router(auth_router,prefix=f"/auth/{version}/user",tags=["User"])


