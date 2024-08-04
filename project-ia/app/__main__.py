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
tasks_ids = []

async def process_queue():
    while True:
        task_id, task = await queue.get()
        if callable(task) and task_id not in tasks_ids:
            try:
                print(f"Processing task {task_id} 👀")
                await task()
            except Exception as e:
                print(f"Error processing task {task_id}: {e}")
            finally:
                queue.task_done()
        else:
            print(f"Task {task_id} is not callable")

app.mount(
    "/app/public",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "app/public"),
    name="public",
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())

init_routes(app, queue)                                                                                                                                                                                                                                                                                  