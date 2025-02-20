from pydantic import BaseModel

class AnimalResponse(BaseModel):
    id: str
    name: str
    species: str
    age: int
