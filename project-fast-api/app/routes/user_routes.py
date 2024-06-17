from fastapi import APIRouter
from fastapi import HTTPException
from app.database import connect_db, disconnect_db
from app.services import auth_services
from fastapi.responses import JSONResponse
from app.services import email_services
import random


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
        query = "INSERT INTO users (name, email, password, role) VALUES ($1, $2, $3, $4) RETURNING *"
        password_hash = auth_services.get_password_hash(user["password"])
        user = await conn.fetchrow(query, user["name"], user["email"], password_hash, user["role"])
        jwt_token = auth_services.create_access_token(data={"sub": user['role']})
        user = dict(user)
        user["jwt_token"] = jwt_token
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.post("/users/login")
async def login_user(user: dict):
    conn = await connect_db()
    try:
        query = "SELECT * FROM users WHERE email = $1"
        user_db = await conn.fetchrow(query, user["email"])
        if user_db and auth_services.verify_password(user["password"], user_db["password"]):
            jwt_token = auth_services.create_access_token(data={"sub": user_db['role']})
            user_db = dict(user_db)
            user_db["jwt_token"] = jwt_token
            return user_db
        else:
            return JSONResponse(
                status_code= 400,
                content={
                "status": 400,
                "detail": "Invalid credentials"
                },
            )
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
        
@router.post("/users/forgot-password")
async def forgot_password(user: dict):
    conn = await connect_db()
    try:
        query = "SELECT * FROM users WHERE email = $1"
        user_db = await conn.fetchrow(query, user["email"])
        query = "SELECT * FROM code WHERE user_id = $1 ORDER BY id DESC LIMIT 1"
        code_db = await conn.fetchrow(query, user_db["id"])
        if not code_db:
            raise HTTPException(status_code=404, detail="code not found")
        if code_db["code"] == user["code"]:
            new_password = user["password"]
            password_hash = auth_services.get_password_hash(new_password)
            query = "UPDATE users SET password = $1 WHERE email = $2 RETURNING *"
            user_db = await conn.fetchrow(query, password_hash, user["email"])
            jwt_token = auth_services.create_access_token(data={"sub": user_db['role']})
            return JSONResponse(
                status_code= 200,
                content={
                "status": 200,
                "detail": "Password updated",
                "new_password": new_password,
                "jwt_token": jwt_token
                },
            )
        else:
            return JSONResponse(
                status_code= 400,
                content={
                "status": 400,
                "detail": "Invalid code"
                },
            )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await disconnect_db(conn)
        
@router.post("/users/send-email")
async def send_email(user: dict):
    try:
        code_random = random.randint(10000, 99999)
        conn = await connect_db()
        query = "SELECT * FROM users WHERE email = $1"
        user_db = await conn.fetchrow(query, user["email"])
        if not user_db:
            raise HTTPException(status_code=404, detail="user not found")
        query = "INSERT INTO code (user_id, code) VALUES ($1, $2) RETURNING *"
        await conn.fetchrow(query, user_db["id"], code_random)
        await disconnect_db(conn)
        
        email_services.send_email(user["email"], "Cambiar Contraseña", "Tu código de verificación es: " + str(code_random))
        return JSONResponse(
            status_code= 200,
            content={
            "status": 200,
            "detail": "Email sent"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))