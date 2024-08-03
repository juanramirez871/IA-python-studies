from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import init_routes
from fastapi.staticfiles import StaticFiles
from pathlib import Path

load_dotenv()
app = FastAPI()
port = 3000

app.mount(
    "/app/public",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "app/public"),
    name="public",
)

init_routes(app)                                                                                                                                                                                                                                                                                  