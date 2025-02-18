from pydantic import BaseModel
from app.models.fuel_consumption import FuelConsumption


class Engine(BaseModel):
    id: int
    horse_power: int
    displacement: float
    cylinders: int
    fuel_type: str
    transmission: str
    fuel_consumption: FuelConsumption