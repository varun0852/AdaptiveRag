from src.db.mongo_client import chat_collection
from src.core.logger import get_logger

logger = get_logger(__name__)


async def save_message(session_id: str, role: str, content: str):
    try:
        await chat_collection.insert_one({
            "session_id": session_id,
            "role": role,
            "content": content,
        })
    except Exception as e:
        logger.error(f"Failed to save message: {e}")


async def get_history(session_id: str, limit: int = 10) -> list:
    try:
        cursor = chat_collection.find(
            {"session_id": session_id},
            sort=[("_id", -1)],
            limit=limit
        )
        messages = await cursor.to_list(length=limit)
        messages.reverse()
        return [{"role": m["role"], "content": m["content"]} for m in messages]
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        return []