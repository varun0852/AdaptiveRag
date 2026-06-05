from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from src.config.settings import QDRANT_URL, QDRANT_API_KEY, QDRANT_DOCS_COLLECTION
from src.core.logger import get_logger

logger = get_logger(__name__)

# Free embeddings - downloads 90MB on first run only
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Connect to Qdrant Cloud
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Create collection if it doesn't exist
try:
    qdrant_client.get_collection(QDRANT_DOCS_COLLECTION)
    logger.info(f"Collection '{QDRANT_DOCS_COLLECTION}' already exists.")
except Exception:
    qdrant_client.create_collection(
        collection_name=QDRANT_DOCS_COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    logger.info(f"Created collection '{QDRANT_DOCS_COLLECTION}'.")

# Vector store and retriever
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=QDRANT_DOCS_COLLECTION,
    embedding=embeddings,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})