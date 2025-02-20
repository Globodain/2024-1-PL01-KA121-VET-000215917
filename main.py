from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router as animals_router

app = FastAPI(title="Animal API")

app.include_router(animals_router, prefix="/animals", tags=["Animals"])

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
