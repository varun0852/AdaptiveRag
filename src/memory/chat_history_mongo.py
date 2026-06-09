from src.db.mongo_client import db
from src.core.logger import get_logger

logger = get_logger(__name__)

async def save_message(session_id: str, role: str, content: str):
    if db is None:
        logger.warning("MongoDB unavailable — skipping save.")
        return
    try:
        collection = db["chat_history"]
        await collection.insert_one({
            "session_id": session_id,
            "role": role,
            "content": content
        })
    except Exception as e:
        logger.error(f"Failed to save message: {e}")

async def get_history(session_id: str):
    if db is None:
        logger.warning("MongoDB unavailable — returning empty history.")
        return []
    try:
        collection = db["chat_history"]
        cursor = collection.find(
            {"session_id": session_id},
            sort=[("_id", 1)]
        )
        return await cursor.to_list(length=100)
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        return []
