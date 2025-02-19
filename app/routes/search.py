from datetime import datetime
from typing import Literal

from db import cars_collection
from fastapi import APIRouter
from models.car import Car

router = APIRouter()

@router.get("/search", response_model=list[Car], name="Search for cars with specific parameters")
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
  price_to: int = None,
  sort_by: Literal["brand", "model", "year", "milage", "price"] = None,
  sort_order: Literal["asc", "desc"] = None):

  query = {}

  for field, value in [("brand", brand), ("model", model), ("year", year), ("milage", milage), ("price", price)]:
    if value is not None:
      query[field] = value
  
  if year_from is not None or year_to is not None:
    query["year"] = {"$gte": year_from or 1900, "$lte": year_to or datetime.now().year}

  if milage_from is not None or milage_to is not None:
    query["milage"] = {"$gte": milage_from or 0, "$lte": milage_to or 9999999}

  if price_from is not None or price_to is not None:
    query["price"] = {"$gte": price_from or 0, "$lte": price_to or 9999999}

  sort_order = 1 if sort_order == "asc" else -1
  sort_criteria = [(sort_by, sort_order)] if sort_by else None

  cars = cars_collection.find(query).sort(sort_criteria) if sort_criteria else cars_collection.find(query)
  cars = [car for car in cars]

  return cars