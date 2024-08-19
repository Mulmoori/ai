# app/routers/update_router.py

from fastapi import APIRouter, HTTPException
from app.models.request_models import UpdateVectorStoreRequest
from app.services.chroma_service import (
    load_or_create_vectorstore,
    append_to_vectorstore,
)
from app.services.chroma_client import get_chroma_client  # 클라이언트 가져오기

router = APIRouter()


@router.post("/update_vectorstore")
async def update_vectorstore(request: UpdateVectorStoreRequest):
    try:
        # ID를 문자열로 변환하고, Chroma의 컬렉션 이름 요구사항을 충족하도록 조정
        id_str = f"collection_{int(request.id)}"

        # ID로 벡터 스토어 로드 또는 생성
        chroma_client = get_chroma_client()
        print("🔧 벡터 스토어 ${chroma_client}")
        vectorstore = load_or_create_vectorstore(id_str, chroma_client)

        # 벡터 스토어에 질문 및 답변 추가
        append_to_vectorstore(vectorstore, request.question, request.answer)

        return {"message": "Vector store updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
