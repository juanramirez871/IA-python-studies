from fastapi import APIRouter
from fastapi import HTTPException
from app.database import connect_db, disconnect_db

router = APIRouter()


@router.get("/tasks/{item_id}")
async def read_task(item_id: int):
    conn = await connect_db()
    try:
        query = "SELECT * FROM items WHERE id = $1"
        item = await conn.fetchrow(query, item_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    finally:
        await disconnect_db(conn)
