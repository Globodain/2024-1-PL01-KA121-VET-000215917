from db import cars_collection
from fastapi import APIRouter, HTTPException
from models.car import Car

router = APIRouter()

@router.get("/cars",  response_model=list[Car])
def get_cars():
    cars = cars_collection.find()
    cars = [car for car in cars]

    return cars


@router.get("/cars/{brand}", response_model=list[Car])
def get_cars_by_brand(brand: str):
    cars = cars_collection.find({"brand": brand})
    cars = [car for car in cars]

    if cars:
        return cars
    raise HTTPException(status_code=404, detail="Car not found")


@router.get("/cars/{brand}/{model}", response_model=Car)
def get_car(brand: str, model: str):
    car = cars_collection.find_one({"brand": brand, "model": model})
    if car:
        return car
    raise HTTPException(status_code=404, detail="Car not found")


@router.post("/cars")
def create_car(car: Car):
    if cars_collection.find_one({"brand": car.brand, "model": car.model}):
        raise HTTPException(status_code=400, detail="Car already exists")
    cars_collection.insert_one(car.model_dump(by_alias=True))
    raise HTTPException(status_code=201, detail="Car created")



