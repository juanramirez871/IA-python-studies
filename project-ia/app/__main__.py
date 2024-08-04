from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import init_routes
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import asyncio

load_dotenv()
app = FastAPI()
port = 3000

queue = asyncio.Queue()

async def process_queue():
    while True:
        task = await queue.get()
        try:
            print("Processing task 👀")
            await task()
        finally:
            print("Task done ✅")
            queue.task_done()

app.mount(
    "/app/public",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "app/public"),
    name="public",
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())

init_routes(app, queue)                                                                                                                                                                                                                                                                                  