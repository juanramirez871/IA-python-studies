from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def message():
    return 'nice bro on route genre'