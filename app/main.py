from fastapi import FastAPI
from routes.cars import router as cars_router
from routes.search import router as search_router

app = FastAPI(title="Car API")

app.include_router(cars_router)
app.include_router(search_router)