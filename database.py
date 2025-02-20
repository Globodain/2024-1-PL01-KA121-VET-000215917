from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017/admin"
DATABASE_NAME = "admin"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
animals_collection = db["animals_collection"]
