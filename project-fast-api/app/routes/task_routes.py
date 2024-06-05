from fastapi import APIRouter
from fastapi import HTTPException
from app.database import connect_db, disconnect_db

router = APIRouter()


@router.get("/tasks/{item_id}")
async def read_task(item_id: int):
    conn = await connect_db()
    try:
        query = "SELECT * FROM tasks WHERE id = $1"
        item = await conn.fetchrow(query, item_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    finally:
        await disconnect_db(conn)
        
@router.get("/tasks")
async def read_tasks():
    conn = await connect_db()
    try:
        query = "SELECT * FROM tasks"
        items = await conn.fetch(query)
        return [dict(item) for item in items]
    finally:
        await disconnect_db(conn)
        
@router.post("/tasks")
async def create_task(item: dict):
    conn = await connect_db()
    try:
        query = "INSERT INTO tasks (title, description, team_id) VALUES ($1, $2, $3) RETURNING *"
        item = await conn.fetchrow(query, item["name"], item["description"], item["team_id"])
        return dict(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)

@router.put("/tasks/{item_id}")
async def update_task(item_id: int, item: dict):
    conn = await connect_db()
    try:
        query = "UPDATE tasks SET title = $1, description = $2, team_id = $3 WHERE id = $4 RETURNING *"
        item = await conn.fetchrow(query, item["name"], item["description"], item["team_id"], item_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)