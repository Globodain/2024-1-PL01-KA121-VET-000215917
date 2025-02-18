from pydantic import BaseModel
from app.models.engine import Engine
from app.models.range import Range


class Car(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    milage: float
    avg_price: float
    engine: Engine
    range: Range
    seats: int
    doors: int
    trunk_capacity: float
    max_speed: int
    acceleration: float
    fuel_tank_capacity: float