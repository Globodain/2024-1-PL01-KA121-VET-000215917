from fastapi import FastAPI
from routes.cars import router as cars_router

app = FastAPI(title="Car API")

@app.get("/")
def read_root():
    return {"Welcome in the Car API"}

app.include_router(cars_router)