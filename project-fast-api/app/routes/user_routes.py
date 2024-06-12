from fastapi import APIRouter
from fastapi import HTTPException
from app.database import connect_db, disconnect_db
from app.services import auth_services

router = APIRouter()


@router.get("/users/{user_id}")
async def read_users(user_id: int):
    conn = await connect_db()
    try:
        query = "SELECT * FROM users WHERE id = $1"
        item = await conn.fetchrow(query, user_id)
        if item:
            return dict(item)
        else:
            raise HTTPException(status_code=404, detail="user not found")
    finally:
        await disconnect_db(conn)
        
@router.get("/users")
async def read_users():
    conn = await connect_db()
    try:
        query = "SELECT * FROM users"
        items = await conn.fetch(query)
        return [dict(item) for item in items]
    finally:
        await disconnect_db(conn)
        
@router.post("/users")
async def create_user(user: dict):
    conn = await connect_db()
    try:
        print(user)
        query = "INSERT INTO users (name, email, password, role) VALUES ($1, $2, $3, $4) RETURNING *"
        user = await conn.fetchrow(query, user["name"], user["email"], user["password"], user["role"])
        jwt_token = auth_services.create_access_token(data={"sub": user['role']})
        user = dict(user)
        user["jwt_token"] = jwt_token
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.put("/users/{user_id}")
async def update_user(user_id: int, user: dict):
    conn = await connect_db()
    try:
        query = "UPDATE users SET name = $1, email = $2, password = $3, role = $4 WHERE id = $5 RETURNING *"
        user = await conn.fetchrow(query, user["name"], user["email"], user["password"], user["role"], user_id)
        if user:
            return dict(user)
        else:
            raise HTTPException(status_code=404, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = await connect_db()
    try:
        query = "DELETE FROM users WHERE id = $1 RETURNING *"
        user = await conn.fetchrow(query, user_id)
        if user:
            return dict(user)
        else:
            raise HTTPException(status_code=404, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)