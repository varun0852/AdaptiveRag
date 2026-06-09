import motor.motor_asyncio
from src.config.settings import MONGODB_URL, MONGODB_DB_NAME
from src.core.logger import get_logger

logger = get_logger(__name__)

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    db = client[MONGODB_DB_NAME]
    logger.info("MongoDB client initialized.")
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")
    db = None
