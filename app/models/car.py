from pydantic import BaseModel, Field
from models.range import Range


class Car(BaseModel):
    brand: str
    model: str
    year: int
    milage: int
    avg_price: int
    gears: int
    range: Range
    seats: int
    doors: int
    trunk_capacity: float
    max_speed: int
    acceleration: float

    horse_power: int
    displacement: float
    cylinders: int
    fuel_type: str
    transmission: str

    fuel_consumption_city: float
    fuel_consumption_highway: float
    fuel_consumption_combined: float
    fuel_tank_capacity: float

    range_city: float
    range_highway: float
    range_combined: float