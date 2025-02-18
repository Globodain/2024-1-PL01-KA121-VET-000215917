from pydantic import BaseModel, Field


class Car(BaseModel):
    brand: str
    model: str
    year: int = Field(..., ge=1900)
    milage: int = Field(..., ge=0)
    avg_price: int = Field(..., ge=0)
    gears: int = Field(..., ge=1)
    seats: int = Field(..., ge=1)
    doors: int = Field(..., ge=1)
    trunk_capacity: float = Field(..., ge=0)
    max_speed: int = Field(..., ge=0)
    acceleration: float = Field(..., ge=0)

    horse_power: int = Field(..., ge=0)
    displacement: float = Field(..., ge=0)
    cylinders: int = Field(..., ge=0)
    fuel_type: str = Field(..., min_length=3)
    transmission: str = Field(..., min_length=3)

    fuel_consumption_city: float = Field(..., ge=0)
    fuel_consumption_highway: float = Field(..., ge=0)
    fuel_consumption_combined: float = Field(..., ge=0)
    fuel_tank_capacity: float = Field(..., ge=0)

    range_city: float = Field(..., ge=0)
    range_highway: float = Field(..., ge=0)
    range_combined: float = Field(..., ge=0)