from fastapi import APIRouter
from fastapi import HTTPException
from app.database import connect_db, disconnect_db

router = APIRouter()


@router.get("/teams/{team_id}")
async def read_task(team_id: int):
    conn = await connect_db()
    try:
        query = "SELECT * FROM teams WHERE id = $1"
        item = await conn.fetchrow(query, team_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="team not found")
    finally:
        await disconnect_db(conn)

@router.get("/teams")
async def read_tasks():
    conn = await connect_db()
    try:
        query = "SELECT * FROM teams"
        items = await conn.fetch(query)
        return [dict(item) for item in items]
    finally:
        await disconnect_db(conn)
        
@router.post("/teams")
async def create_task(team: dict):
    conn = await connect_db()
    try:
        query = "INSERT INTO teams (name) VALUES ($1) RETURNING *"
        team = await conn.fetchrow(query, team["name"])
        return dict(team)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.put("/teams/{task_id}")
async def update_task(task_id: int, team: dict):
    conn = await connect_db()
    try:
        query = "UPDATE teams SET name = $1 WHERE id = $2 RETURNING *"
        team = await conn.fetchrow(query, team["name"], task_id)
        if team:
            return dict(team)
        else:
            raise HTTPException(status_code=404, detail="team not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.delete("/teams/{task_id}")
async def delete_task(task_id: int):
    conn = await connect_db()
    try:
        query = "DELETE FROM teams WHERE id = $1"
        await conn.execute(query, task_id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.get("/teams/{team_id}/tasks")
async def read_tasks(team_id: int):
    conn = await connect_db()
    try:
        query = "SELECT * FROM tasks WHERE team_id = $1"
        items = await conn.fetch(query, team_id)
        return [dict(item) for item in items]
    finally:
        await disconnect_db(conn)
        
@router.post("/teams/{team_id}/tasks")
async def create_task(team_id: int, item: dict):
    conn = await connect_db()
    try:
        query = "INSERT INTO tasks (title, description, team_id) VALUES ($1, $2, $3) RETURNING *"
        item = await conn.fetchrow(query, item["name"], item["description"], team_id)
        return dict(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.put("/teams/{team_id}/tasks/{task_id}")
async def update_task(team_id: int, task_id: int, item: dict):
    conn = await connect_db()
    try:
        query = "UPDATE tasks SET title = $1, description = $2, team_id = $3 WHERE id = $4 RETURNING *"
        item = await conn.fetchrow(query, item["name"], item["description"], team_id, task_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.delete("/teams/{team_id}/tasks/{task_id}")
async def delete_task(team_id: int, task_id: int):
    conn = await connect_db()
    try:
        query = "DELETE FROM tasks WHERE id = $1 RETURNING *"
        item = await conn.fetchrow(query, task_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.get("/teams/{team_id}/tasks/{task_id}")
async def read_task(team_id: int, task_id: int):
    conn = await connect_db()
    try:
        query = "SELECT * FROM tasks WHERE id = $1 AND team_id = $2"
        item = await conn.fetchrow(query, task_id, team_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="task not found")
    finally:
        await disconnect_db(conn)