from fastapi import APIRouter, HTTPException
from db import cars_collection
from models.car import Car

router = APIRouter()

@router.get("/cars")
def get_cars():
    cars = cars_collection.find()
    return cars

@router.get("/cars/{brand}")
def get_car(brand: str):
    car = cars_collection.find_one({"brand": brand})
    if car:
        return car
    raise HTTPException(status_code=404, detail="Car not found")

@router.post("/cars")
def create_car(car: Car):
    if cars_collection.find_one({"brand": car.brand, "model": car.model}):
        raise HTTPException(status_code=400, detail="Car already exists")
    
  
    cars_collection.insert_one(car.model_dump())
    return car

