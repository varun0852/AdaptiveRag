import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.rag.retriever_setup import vectorstore
from src.core.logger import get_logger

logger = get_logger(__name__)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


async def upload_document(file_bytes: bytes, filename: str, description: str) -> bool:
    try:
        suffix = ".pdf" if filename.endswith(".pdf") else ".txt"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)

        docs = loader.load()

        for doc in docs:
            doc.metadata["description"] = description
            doc.metadata["filename"] = filename

        chunks = splitter.split_documents(docs)
        vectorstore.add_documents(chunks)

        os.unlink(tmp_path)
        logger.info(f"Uploaded '{filename}' — {len(chunks)} chunks indexed.")
        return True

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return False
    