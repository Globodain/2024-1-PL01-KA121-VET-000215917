from pydantic import BaseModel


class Range(BaseModel):
    city: float
    highway: float
    combined: float