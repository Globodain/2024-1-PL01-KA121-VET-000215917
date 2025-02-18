from typing import Union
from fastapi import FastAPI
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["cars"]
col = db["cars"]

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
