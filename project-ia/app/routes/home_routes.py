from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/public/views")
    
@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request}
    )