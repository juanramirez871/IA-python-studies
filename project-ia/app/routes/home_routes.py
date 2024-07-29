from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {
            "title": "My first IA project 🧠",
            "description": "i dont know what to do 🧐",
            "author": "Juan 🧙‍♂️",
            "server": f"Server is running done 🤖"
            }