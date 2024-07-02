from fastapi import FastAPI
from routers import init_routes
from contextlib import asynccontextmanager
import database.models.book as Book
import database.models.genre as Genre
import database.config as database

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with database.engine.begin() as conn:
        await conn.run_sync(Book.Base.metadata.create_all)
        await conn.run_sync(Genre.Base.metadata.create_all)
    yield

app.router.lifespan_context = lifespan
init_routes(app)