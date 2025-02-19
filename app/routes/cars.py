from db import cars_collection
from fastapi import APIRouter, HTTPException
from models.car import Car

router = APIRouter()

@router.get("/search", response_model=list[Car])
def search_cars(brand: str = None, model: str = None, year: int = None, milage: int = None, price: int = None):
    query = {}
    if brand:
        query["brand"] = brand
    if model:
        query["model"] = model
    if year:
        query["year"] = year
    if milage:
        query["milage"] = milage
    if price:
        query["price"] = price

    print(query)
    cars = cars_collection.find(query)
    cars = [car for car in cars]

    return cars


@router.get("/cars",  response_model=list[Car])
def get_all_cars():
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


@router.delete("/cars/{brand}/{model}")
def delete_car(brand: str, model: str):
    if cars_collection.find_one({"brand": brand, "model": model}):
        cars_collection.delete_one({"brand": brand, "model": model})
        raise HTTPException(status_code=200, detail="Car deleted")
    raise HTTPException(status_code=404, detail="Car not found")


@router.put("/cars/{brand}/{model}")
def update_car(brand: str, model: str, car: Car):
    if cars_collection.find_one({"brand": brand, "model": model}):
        car_data = car.model_dump(by_alias=True)
        if "_id" in car_data:
            del car_data["_id"]
        cars_collection.update_one({"brand": brand, "model": model}, {"$set": car_data})
        raise HTTPException(status_code=200, detail="Car updated")
    raise HTTPException(status_code=404, detail="Car not found")

