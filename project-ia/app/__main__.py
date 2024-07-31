from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import init_routes

load_dotenv()
app = FastAPI()
port = 3000

init_routes(app)