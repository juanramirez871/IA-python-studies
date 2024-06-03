from fastapi import HTTPException
import asyncpg
import os
import importlib

DATABASE_URL = "postgresql://juan:123@localhost:5433/test"

async def connect_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"⚠️ Error connecting to the database: {e}")

async def disconnect_db(conn):
    try:
        await conn.close()
    except Exception as e:
        print(f"⚠️ Error disconnecting from the database: {e}")
    
async def run_migrations():
    
    print("Running migrations...")
    routers_dir = os.path.join(os.path.dirname(__file__), "migrations/")
    for filename in os.listdir(routers_dir):
        
        if filename.endswith(".py") and filename != "__init__.py":
            
            print(f"Running migration for {filename}...")
            module_name = f"app.database.migrations.{filename[:-3]}"
            module = importlib.import_module(module_name)
            try:
                query = module.migrate()
                conn = await connect_db()
                await conn.execute(query)
                print(f"Migration for {module_name} ran successfully ✅")
            
            except Exception as e:
                print(f"Error running migration for {module_name}: {e} ❗")
                
            finally:
                await disconnect_db(conn)
    
exported = [connect_db, disconnect_db]