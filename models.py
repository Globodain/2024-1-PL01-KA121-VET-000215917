from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Animal(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    age: int
    description: Optional[str] = None

    class Config:
        json_encoders = {
            ObjectId: str
        }
    def animal_from_mongo(animal_data):
        return Animal(id=str(animal_data["_id"]),
                    name=animal_data["name"],
                    type=animal_data["type"],
                    age=animal_data["age"],
                    description=animal_data.get("description"))