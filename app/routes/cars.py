from fastapi import APIRouter, HTTPException
from db import cars_collection
from models.car import Car

router = APIRouter()

@router.get("/cars")
def get_cars():
    cars = cars_collection.find()
    return cars

@router.post("/cars")
def create_car(car: Car):
    cars_collection.insert_one(car.model_dump())
    return car