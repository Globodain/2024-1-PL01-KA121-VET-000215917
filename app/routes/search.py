from datetime import datetime
from typing import Literal, Optional

from db import cars_collection
from fastapi import APIRouter, HTTPException
from models.car import Car

router = APIRouter()

order_mapping = {
      'brand_asc': ('brand', 1),
      'brand_desc': ('brand', -1),
      'model_asc': ('model', 1),
      'model_desc': ('model', -1),
      'year_asc': ('year', 1),
      'year_desc': ('year', -1),
      'milage_asc': ('milage', 1),
      'milage_desc': ('milage', -1),
      'price_asc': ('price', 1),
      'price_desc': ('price', -1),
      'maxspeed_asc': ('max_speed', 1),
      'maxspeed_desc': ('max_speed', -1),
      'acceleration_asc': ('acceleration', 1),
      'acceleration_desc': ('acceleration', -1),
      'horsepower_asc': ('horse_power', 1),
      'horsepower_desc': ('horse_power', -1),
      'consumption_combined_asc': ('fuel_consumption_combined', 1),
      'consumption_combined_desc': ('fuel_consumption_combined', -1),
      'range_combined_asc': ('range_combined', 1),
      'range_combined_desc': ('range_combined', -1),
}

@router.get('/cars/search', response_model=list[Car], name='Advanced search for cars with specific parameters')
def search_cars(
  limit: int = 0,
  brand: Optional[str] = None,
  model: Optional[str] = None,
  year: Optional[int] = None,
  milage: Optional[int] = None,
  vin: Optional[str] = None,
  price: Optional[int] = None, 
  year_from: Optional[int] = None, 
  year_to: Optional[int] = None, 
  milage_from: Optional[int] = None,
  milage_to: Optional[int] = None, 
  price_from: Optional[int] = None, 
  price_to: Optional[int] = None,
  # sort_by: Optional[Literal['brand', 'model', 'year', 'milage', 'price']] = None,
  sort_by: Optional[Literal['brand_asc',
                            'brand_desc',
                            'model_asc',
                            'model_desc',
                            'year_asc',
                            'year_desc',
                            'milage_asc',
                            'milage_desc',
                            'price_asc',
                            'price_desc',
                            'maxspeed_asc',
                            'maxspeed_desc',
                            'acceleration_asc',
                            'acceleration_desc',
                            'horsepower_asc',
                            'horsepower_desc',
                            'consumption_combined_asc',
                            'consumption_combined_desc',
                            'range_combined_asc',
                            'range_combined_desc']] = None):

  try:
    query = {}

    for field, value in [('brand', brand), ('model', model), ('year', year), ('milage', milage), ('price', price), ('vin', vin)]:
      if value is not None:
        query[field] = value
    
    if year_from is not None or year_to is not None:
      query['year'] = {'$gte': year_from or 1900, '$lte': year_to or datetime.now().year}

    if milage_from is not None or milage_to is not None:
      query['milage'] = {'$gte': milage_from or 0, '$lte': milage_to or 9999999}

    if price_from is not None or price_to is not None:
      query['price'] = {'$gte': price_from or 0, '$lte': price_to or 9999999}
    
    sort_criteria = None

    if sort_by:
      sort_criteria = [order_mapping[sort_by]]

    cars = cars_collection.find(query).sort(sort_criteria).limit(limit) if sort_criteria else cars_collection.find(query).limit(limit)
    cars = [car for car in cars]

    return cars

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))