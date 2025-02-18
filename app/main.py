from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from routes.cars import router as cars_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello World"}

app.include_router(cars_router)