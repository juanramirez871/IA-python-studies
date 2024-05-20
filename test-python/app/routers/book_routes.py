from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def message():
    return 'nice bro'