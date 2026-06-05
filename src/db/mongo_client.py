import motor.motor_asyncio
from src.config.settings import MONGODB_URL, MONGODB_DB_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_DB_NAME]
chat_collection = db["chat_history"]