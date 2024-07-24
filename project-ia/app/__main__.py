from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import init_routes

load_dotenv()
app = FastAPI()
port = 3000

init_routes(app)

if __name__ == "__main__":
    import uvicorn
    print(f"Server is running on port {port} 🤖")
    uvicorn.run(app, host="0.0.0.0", port=port)
