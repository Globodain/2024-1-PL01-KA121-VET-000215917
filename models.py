from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from enum import Enum
from fastapi import Query


class Car(BaseModel):
    id: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    production_year: Optional[int] = None
    price: Optional[float] = None
    horsepower: Optional[int] = None
    engine_displacement: Optional[float] = None
    dors: Optional[int] = 5  
    color: Optional[str] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    fuel_consumption: Optional[float] = None
    max_speed: Optional[int] = None
    image: Optional[str] = None
    transmission: Optional[str] = None
    drivetrain: Optional[str] = None
    seats: Optional[int] = None
    description: Optional[str] = None

    class Config:
        json_encoders = {
            ObjectId: str
        }

class SortFields(str, Enum):
    production_year = "production_year" 
    price = "price"
    horsepower = "horsepower"
    mileage = "mileage"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class CarSearchParams(BaseModel):
    brand: Optional[str] = Query(None, min_length=1, description="Brand of the car")
    model: Optional[str] = Query(None, description="Model of the car")
    year: Optional[int] = Query(None, description="Production year of the car")
    min_price: Optional[float] = Query(None, description="Minimum price of the car")
    max_price: Optional[float] = Query(None, description="Maximum price of the car")
    color: Optional[str] = Query(None, description="Color of the car")
    mileage: Optional[int] = Query(None, description="Mileage of the car")
    limit: int = Query(10, description="Number of results to return")
    sort_by: Optional[SortFields] = Query(None, description="Field to sort by")
    sort_order: Optional[SortOrder] = Query(SortOrder.asc, description="Sort order (asc or desc)")