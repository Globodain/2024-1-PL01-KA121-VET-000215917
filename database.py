from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI)
database = client.animals_db 