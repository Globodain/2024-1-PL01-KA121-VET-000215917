from fastapi import APIRouter, HTTPException
from database import animals_collection
from models import Animal
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/")
async def root():
    return "Hello World"

#Add new animal
@router.post("/animals/", response_model=Animal)
async def add_animal(animal: Animal):
    new_animal = await animals_collection.insert_one(animal.model_dump())
    if new_animal.inserted_id:
        return {**animal.model_dump(), "id": str(new_animal.inserted_id)}
    raise HTTPException(status_code=400, detail="Failed to add animal")

#Get all animals
@router.get("/animals/")
async def get_animals(limit: int = 10, skip: int = 0):
    animals_data = await animals_collection.find().skip(skip).limit(limit).to_list(None)
    return [Animal.animal_from_mongo(animal) for animal in animals_data]

#Get specified animal by id
@router.get("/animals/{animal_id}")
async def get_animal(animal_id: str):
    animal_data = await animals_collection.find_one({"_id": ObjectId(animal_id)})
    if animal_data:
        animal = Animal.animal_from_mongo(animal_data)
        return animal
    raise HTTPException(status_code=404, detail="Animal not found")

#Get specified animals by filters
@router.get("/animals/filter/")
async def filter_animals(name: str = None, type: str = None, min_age: int = None, max_age: int = None):
    query = {}
    if name:
        query['name'] = name
    if type:
        query["type"] = type
    if min_age is not None:
        query["age"] = {"$gte": min_age}
    if max_age is not None:
        query["age"] = query.get("age", {})
        query["age"]["$lte"] = max_age
    
    animals_data = await animals_collection.find(query).to_list(None)
    return [Animal.animal_from_mongo(animal) for animal in animals_data]

#Delete animal by id
@router.delete("/animals/{animal_id}")
async def delete_animal(animal_id: str):
    animal_data = await animals_collection.find_one({"_id": ObjectId(animal_id)})
    if animal_data is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    result = await animals_collection.delete_one({"_id": ObjectId(animal_id)})
    if result.deleted_count:
        return Animal.animal_from_mongo(animal_data)
    raise HTTPException(status_code=404, detail="Animal not deleted")

#Update an animal
@router.put("/animals/{animal_id}", response_model=Animal)
async def update_animal(animal_id: str, animal_update: Animal):
    update_data = {k: v for k, v in animal_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    result = await animals_collection.update_one(
        {"_id": ObjectId(animal_id)}, {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found or no changes applied")
    
    updated_animal = await animals_collection.find_one({"_id": ObjectId(animal_id)})
    return Animal.animal_from_mongo(updated_animal)