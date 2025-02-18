from pydantic import BaseModel


class FuelConsumption(BaseModel):
  city: float
  highway: float
  combined: float
