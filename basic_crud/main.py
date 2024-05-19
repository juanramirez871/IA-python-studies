from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Base de datos simulada
fake_db: List[Item] = []

# Crear un nuevo item
@app.post("/items/", response_model=str)
def create_item(item: Item):
    fake_db.append(item)
    return "added item successfully"

# Leer todos los items
@app.get("/items/", response_model=List[Item])
def read_items():
    return fake_db

# Leer un item por ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in fake_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Actualizar un item por ID
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(fake_db):
        if item.id == item_id:
            fake_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Borrar un item por ID
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for index, item in enumerate(fake_db):
        if item.id == item_id:
            deleted_item = fake_db.pop(index)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
