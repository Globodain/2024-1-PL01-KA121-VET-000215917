from fastapi import FastAPI, HTTPException, Query, Depends
from models import Car, SortFields, SortOrder, CarSearchParams
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import logging

app = FastAPI(title="Car API")

logging.basicConfig(level=logging.INFO)

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['Carshop']
collection = db['Cars']

@app.post("/cars/", response_model=Car)
async def create_car(car: Car):
    car_data = car.dict()
    result = await collection.insert_one(car_data)
    car_data["id"] = str(result.inserted_id)
    logging.info(f"Car created: {car_data}")
    return car_data

@app.get("/cars/all/", response_model=List[Car])
async def get_all_cars(skip: int = 0, limit: int = 10, sort_by: Optional[SortFields] = None, sort_order: Optional[SortOrder] = SortOrder.asc):
    cars = []
    cursor = collection.find().skip(skip).limit(limit)
    if sort_by:
        order = 1 if sort_order == SortOrder.asc else -1
        cursor = cursor.sort(sort_by.value, order)
    async for car in cursor:
        car["id"] = str(car["_id"])
        del car["_id"]
        cars.append(car)
    logging.info(f"All cars: {cars}")
    return cars

@app.get("/cars/", response_model=List[Car])
async def search_cars(params: CarSearchParams = Depends()):
    query = {}
    if params.brand:
        query["brand"] = {"$regex": params.brand, "$options": "i"}
    if params.model:
        query["model"] = {"$regex": params.model, "$options": "i"}
    if params.year:
        query["production_year"] = params.year
    if params.min_price is not None and params.max_price is not None:
        query["price"] = {"$gte": params.min_price, "$lte": params.max_price}
    elif params.min_price is not None:
        query["price"] = {"$gte": params.min_price}
    elif params.max_price is not None:
        query["price"] = {"$lte": params.max_price}
    if params.color:
        query["color"] = {"$regex": params.color, "$options": "i"}
    if params.mileage:
        query["mileage"] = params.mileage

    logging.info(f"Query: {query}")

    cars = []
    cursor = collection.find(query).limit(params.limit)
    if params.sort_by:
        order = 1 if params.sort_order == SortOrder.asc else -1
        cursor = cursor.sort(params.sort_by.value, order)
    async for car in cursor:
        car["id"] = str(car["_id"])
        del car["_id"]
        cars.append(car)
    logging.info(f"Cars found: {cars}")

    if not cars:
        raise HTTPException(status_code=404, detail="No cars found matching the provided criteria")

    return cars

@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: str, car: Car):
    updated_data = car.dict(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    
    try:
        car_object_id = ObjectId(car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid car ID format")
    
    result = await collection.update_one({"_id": car_object_id}, {"$set": updated_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    
    updated_car = await collection.find_one({"_id": car_object_id})
    updated_car["id"] = str(updated_car["_id"])
    del updated_car["_id"]
    
    logging.info(f"Car updated: {updated_car}")
    return updated_car

@app.delete("/cars/{car_id}", response_model=dict)
async def delete_car(car_id: str):
    try:
        car_object_id = ObjectId(car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid car ID format")
    
    result = await collection.delete_one({"_id": car_object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    
    logging.info(f"Car deleted: {car_id}")
    return {"status": f"Car with ID {car_id} is deleted successfully"}
