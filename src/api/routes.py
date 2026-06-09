from fastapi import APIRouter, UploadFile, File, Header, HTTPException
from src.models.query_request import QueryRequest
from src.rag.graph_builder import rag_graph
from src.rag.document_upload import upload_document
from src.memory.chat_history_mongo import save_message, get_history
from src.core.logger import get_logger

router = APIRouter(prefix="/rag")
logger = get_logger(__name__)

@router.post("/query")
async def query_rag(request: QueryRequest):
    try:
        # Save user message — silently skip if MongoDB fails
        try:
            await save_message(request.session_id, "user", request.query)
        except Exception as mongo_err:
            logger.warning(f"MongoDB save skipped: {mongo_err}")

        result = rag_graph.invoke({
            "query": request.query,
            "session_id": request.session_id,
            "route": None,
            "documents": [],
            "answer": None,
            "rewrite_count": 0,
        })

        answer = result.get("answer", "Sorry, I couldn't find an answer.")

        # Save assistant message — silently skip if MongoDB fails
        try:
            await save_message(request.session_id, "assistant", answer)
        except Exception as mongo_err:
            logger.warning(f"MongoDB save skipped: {mongo_err}")

        return {"result": {"type": "ai", "content": answer}}

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/upload")
async def upload_doc(
    file: UploadFile = File(...),
    x_description: str = Header(...),
):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files allowed.")
    file_bytes = await file.read()
    success = await upload_document(file_bytes, file.filename, x_description)
    if not success:
        raise HTTPException(status_code=500, detail="Document processing failed.")
    return {"status": True}

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        history = await get_history(session_id)
        return {"history": history}
    except Exception as e:
        logger.warning(f"History fetch failed: {e}")
        return {"history": []}
