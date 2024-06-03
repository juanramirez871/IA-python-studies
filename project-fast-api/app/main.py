from fastapi import FastAPI
from app.routes import init_routes
from app.database import run_migrations
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()    
    yield


app.router.lifespan_context = lifespan
init_routes(app)