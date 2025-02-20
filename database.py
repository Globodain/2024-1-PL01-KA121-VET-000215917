from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["animal_db"]
animals_collection = db["animals"]