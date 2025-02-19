from datetime import datetime

from db import cars_collection
from fastapi import APIRouter, HTTPException
from models.car import Car

router = APIRouter()


@router.get("/cars",  response_model=list[Car], description="Get all cars")
def get_all_cars():
    cars = cars_collection.find()
    cars = [car for car in cars]

    return cars


@router.get("/cars/{brand}", response_model=list[Car], description="Get cars by brand")
def get_cars_by_brand(brand: str):
    cars = cars_collection.find({"brand": brand})
    cars = [car for car in cars]

    if cars:
        return cars
    raise HTTPException(status_code=404, detail="Car not found")


@router.get("/cars/{brand}/{model}", response_model=Car, description="Get car by brand and model")
def get_car(brand: str, model: str):
    car = cars_collection.find_one({"brand": brand, "model": model})
    if car:
        return car
    raise HTTPException(status_code=404, detail="Car not found")


@router.post("/cars", description="Create cars")
def create_car(cars: list[Car]):
    cars_added = 0
    for car in cars:
        if cars_collection.find_one({"brand": car.brand, "model": car.model}) == None:
            cars_collection.insert_one(car.model_dump(by_alias=True))
            cars_added += 1

    if cars_added == 0:
        raise HTTPException(status_code=400, detail="Cars already exists")

    raise HTTPException(status_code=201, detail="Cars created: " + str(cars_added) + "/" + str(len(cars)))


@router.delete("/cars/{brand}/{model}", description="Delete car by brand and model")
def delete_car(brand: str, model: str):
    if cars_collection.find_one({"brand": brand, "model": model}):
        cars_collection.delete_one({"brand": brand, "model": model})
        raise HTTPException(status_code=200, detail="Car deleted")
    raise HTTPException(status_code=404, detail="Car not found")


@router.put("/cars/{brand}/{model}", description="Update car by brand and model")
def update_car(brand: str, model: str, car: Car):
    if cars_collection.find_one({"brand": brand, "model": model}):
        car_data = car.model_dump(by_alias=True)

        if "_id" in car_data:
            del car_data["_id"]

        cars_collection.update_one({"brand": brand, "model": model}, {"$set": car_data})
        raise HTTPException(status_code=200, detail="Car updated")
    
    raise HTTPException(status_code=404, detail="Car not found") 