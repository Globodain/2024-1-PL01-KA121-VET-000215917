from datetime import datetime

from db import cars_collection
from fastapi import APIRouter, HTTPException
from models.car import Car

router = APIRouter()

@router.get('/cars', response_model=list[Car], name='Get all cars')
def get_all_cars(limit: int = 0):
    try:
        cars = cars_collection.find().limit(limit) if limit > 0 else cars_collection.find()
        cars = [car for car in cars]
        return cars
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/cars/{vin}', response_model=Car, name='Get car by VIN')
def get_car(vin: str):
    try:
        car = cars_collection.find_one({'vin': vin})
        if car:
            return car
        raise HTTPException(status_code=404, detail='Car not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/cars', name='Create cars')
def create_car(cars: list[Car]):
    try:
        cars_added = 0
        for car in cars:
            if cars_collection.find_one({'vin': car.vin}) is None:
                cars_collection.insert_one(car.model_dump(by_alias=True))
                cars_added += 1

        if cars_added == 0:
            raise HTTPException(status_code=400, detail='Cars already exist')

        return {'detail': f'Cars created: {cars_added}/{len(cars)}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/cars/{vin}', name='Delete car by VIN')
def delete_car(vin: str):
    try:
        if cars_collection.find_one({'vin': vin}):
            cars_collection.delete_one({'vin': vin})
            raise HTTPException(status_code=200, detail='Car deleted')
        raise HTTPException(status_code=404, detail='Car not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/cars/{vin}', name='Update car by VIN')
def update_car(vin: str, update: dict):
    try:
        if cars_collection.find_one({'vin': vin}):
            if not isinstance(update, dict):
                raise HTTPException(status_code=400, detail='Invalid update data')

            update_data = {k: v for k, v in update.items() if k in Car.model_fields}
            if not update_data:
                raise HTTPException(status_code=400, detail='No valid fields to update')

            cars_collection.update_one({'vin': vin}, {'$set': update_data})
            return {'detail': 'Car updated'}

        raise HTTPException(status_code=404, detail='Car not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
