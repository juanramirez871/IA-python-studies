from fastapi import FastAPI
from app.routes import init_routes
from app.database import run_migrations
from contextlib import asynccontextmanager
from app.middlewares.auth_middleware import init_middlewares

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()    
    yield


app.router.lifespan_context = lifespan
init_middlewares(app)
init_routes(app)