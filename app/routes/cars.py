from datetime import datetime

from db import cars_collection
from fastapi import APIRouter, HTTPException
from models.car import Car

router = APIRouter()

@router.get("/search", response_model=list[Car])
def search_cars(
    brand: str = None,
    model: str = None,
    year: int = None,
    milage: int = None,
    price: int = None, 
    year_from: int = None, 
    year_to: int = None, 
    milage_from: int = None,
    milage_to: int = None, 
    price_from: int = None, 
    price_to: int = None):

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

    if year_from or year_to:
        if year_from == None: year_from = 1900
        if year_to == None: year_to = datetime.now().year

        query["year"] = {"$gte": year_from, "$lte": year_to}

    if milage_from or milage_to:
        if milage_from == None: milage_from = 0
        if milage_to == None: milage_to = 9999999

        query["milage"] = {"$gte": milage_from, "$lte": milage_to}

    if price_from or price_to:
        if price_from == None: price_from = 0
        if price_to == None: price_to = 9999999

        query["price"] = {"$gte": price_from, "$lte": price_to}

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
def create_car(cars: list[Car]):
    cars_added = 0
    for car in cars:
        if cars_collection.find_one({"brand": car.brand, "model": car.model}) == None:
            cars_collection.insert_one(car.model_dump(by_alias=True))
            cars_added += 1
    if cars_added == 0:
        raise HTTPException(status_code=400, detail="Cars already exists")
    
    raise HTTPException(status_code=201, detail="Cars created: " + str(cars_added) + "/" + str(len(cars)))

    # if cars_collection.find_one({"brand": car.brand, "model": car.model}):
    #     raise HTTPException(status_code=400, detail="Car already exists")
    # cars_collection.insert_one(car.model_dump(by_alias=True))
    # raise HTTPException(status_code=201, detail="Car created")


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

