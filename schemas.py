from pydantic import BaseModel

class AnimalCreate(BaseModel):
    name: str
    species: str
    age: int
    description: str = None

class AnimalResponse(BaseModel):
    id: str
    name: str
    species: str
    age: int
    description: str = None
    image_url: str = None
