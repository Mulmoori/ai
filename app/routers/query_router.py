# app/routers/query_router.py

from fastapi import APIRouter, HTTPException
from app.models.request_models import QueryRequest
from app.services.chroma_service import load_or_create_vectorstore, query_vectorstore
from app.services.chroma_client import get_chroma_client  # 클라이언트 가져오기

router = APIRouter()


@router.post("/query")
async def process_query(query_request: QueryRequest):
    try:
        id_str = f"collection_{int(query_request.id)}"
        chroma_client = get_chroma_client()  # 클라이언트 가져오기

        vectorstore = load_or_create_vectorstore(id_str, chroma_client)
        answer = query_vectorstore(vectorstore, query_request.question)

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
