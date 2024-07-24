import os
import importlib
from fastapi import FastAPI

def init_routes(app: FastAPI):
    
    routers_dir = os.path.join(os.path.dirname(__file__), "")
    for filename in os.listdir(routers_dir):
        
        if filename.endswith(".py") and filename != "__init__.py":
            
            module_name = f"app.routes.{filename[:-3]}"
            module = importlib.import_module(module_name)
            
            if hasattr(module, "router"):
                app.include_router(module.router)