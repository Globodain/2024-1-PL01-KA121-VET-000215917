from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from crud import create_animal, get_all_animals, get_animal_by_id, update_animal, delete_animal, filter_animals
from schemas import AnimalCreate, AnimalResponse
from typing import List, Optional
import shutil
import os

router = APIRouter(prefix="/animals", tags=["Animals"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=AnimalResponse)
def create_animal_endpoint(
    name: str = Form(...),
    species: str = Form(...),
    age: int = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None)
):
    image_url = None
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"

    animal = AnimalCreate(
        name=name,
        species=species,
        age=age,
        description=description,
        image_url=image_url
    )
    return create_animal(animal)

@router.get("/", response_model=List[AnimalResponse])
def get_all_animals_endpoint():
    return get_all_animals()

@router.get("/filter/", response_model=List[AnimalResponse])
def filter_animals_endpoint(
    name: Optional[str] = Query(None, description="Filter by name"),
    species: Optional[str] = Query(None, description="Filter by species"),
    min_age: Optional[int] = Query(None, description="Filter by minimum age"),
    max_age: Optional[int] = Query(None, description="Filter by maximum age")
):
    return filter_animals(name=name, species=species, min_age=min_age, max_age=max_age)

@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal_by_id_endpoint(animal_id: str):
    animal = get_animal_by_id(animal_id)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal_endpoint(animal_id: str, animal: AnimalCreate):
    updated = update_animal(animal_id, animal)
    if updated is None:
        raise HTTPException(status_code=404, detail="Animal not found or update failed")
    return updated

@router.delete("/{animal_id}")
def delete_animal_endpoint(animal_id: str):
    return delete_animal(animal_id)
