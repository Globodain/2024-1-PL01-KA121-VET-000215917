from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "animals_db"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
animals_collection = database["animals"]