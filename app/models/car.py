from typing import Annotated, Literal

from bson.objectid import ObjectId
from models.model import _ObjectIdPydanticAnnotation
from pydantic import BaseModel, Field

PydanticObjectId = Annotated[
    ObjectId, _ObjectIdPydanticAnnotation
]

class Car(BaseModel):
    id:  PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id', )
    brand: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    vin: str = Field(..., min_length=1, max_length=17)
    year: int = Field(..., ge=1900)
    milage: int = Field(..., ge=0)
    price: int = Field(..., ge=0)
    gears: int = Field(..., ge=1)
    seats: int = Field(..., ge=1)
    doors: int = Field(..., ge=1)
    trunk_capacity: float = Field(..., ge=0)
    max_speed: int = Field(..., ge=0)
    acceleration: float = Field(..., ge=0)

    horse_power: int = Field(..., ge=0)
    displacement: float = Field(..., ge=0)
    cylinders: int = Field(..., ge=0)
    fuel_type: Literal['gasoline', 'diesel', 'hybrid', 'electric', 'hydrogen', 'ethanol', 'biodiesel', 'natural gas'] = Field(...)
    transmission: Literal['manual', 'automatic', 'semi-automatic', 'CVT'] = Field(...)

    fuel_consumption_city: float = Field(..., ge=0)
    fuel_consumption_highway: float = Field(..., ge=0)
    fuel_consumption_combined: float = Field(..., ge=0)
    fuel_tank_capacity: float = Field(..., ge=0)

    range_city: float = Field(..., ge=0)
    range_highway: float = Field(..., ge=0)
    range_combined: float = Field(..., ge=0)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}