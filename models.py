from pydantic import BaseModel
from typing import Optional

class Animal(BaseModel):
    name: str
    species: str
    age: int 
    description: Optional[str] = None