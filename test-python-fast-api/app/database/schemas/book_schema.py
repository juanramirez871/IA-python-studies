from pydantic import BaseModel
from typing import List

class Book_schema(BaseModel):
    title: str
    description: str
