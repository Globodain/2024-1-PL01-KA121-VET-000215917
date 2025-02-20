from fastapi import APIRouter, HTTPException, Form, Query
from models import Animal
from database import database
from bson import ObjectId
from typing import List, Optional

router = APIRouter()

# Helper function for animals
def animal_helper(animal) -> dict:
    return {
        "id": str(animal["_id"]),
        "name": animal["name"],
        "species": animal["species"],
        "age": animal["age"],
        "description": animal.get("description", "")
    }

@router.post("/animals/", response_model=Animal, tags=["Animals"])
async def create_animal(
    name: str = Form(...),
    species: str = Form(...),
    age: int = Form(...),
    description: str = Form(None)
):
    animal_dict = {
        "name": name,
        "species": species,
        "age": age,
        "description": description
    }
    result = await database.animals.insert_one(animal_dict)
    new_animal = await database.animals.find_one({"_id": result.inserted_id})
    return animal_helper(new_animal)

@router.get("/animals/{animal_id}", tags=["Animals"])
async def get_animal(animal_id: str):
    animal = await database.animals.find_one({"_id": ObjectId(animal_id)})
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal_helper(animal)

@router.get("/animals/", tags=["Animals"])
async def get_animals(
    filter_age: Optional[int] = Query(None),
    filter_species: Optional[str] = Query(None),
    search_name: Optional[str] = Query(None)
):
    query = {}

    if filter_age is not None:
        query["age"] = filter_age

    if filter_species:
        query["species"] = {"$regex": filter_species, "$options": "i"}
    
    if search_name:
        query["name"] = {"$regex": search_name, "$options": "i"}

    animals_cursor = database.animals.find(query).sort("name", 1)
    animals = await animals_cursor.to_list(length=100)
    
    if not animals:
        raise HTTPException(status_code=404, detail="No animals found matching your criteria.")

    return [animal_helper(animal) for animal in animals]


@router.put("/animals/{animal_id}", tags=["Animals"])
async def update_animal(animal_id: str, animal: Animal):
    updated_animal = await database.animals.find_one_and_update(
        {"_id": ObjectId(animal_id)},
        {"$set": animal.dict()},
        return_document=True
    )
    if updated_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal_helper(updated_animal)

@router.delete("/animals/{animal_id}", tags=["Animals"])
async def delete_animal(animal_id: str):
    deleted_animal = await database.animals.find_one_and_delete({"_id": ObjectId(animal_id)})
    if deleted_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {"message": f"Animal {deleted_animal['name']} deleted successfully"}