# app/routers/stt_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import rag_pipeline

router = APIRouter()


class STTInput(BaseModel):
    # 사용자가 입력한 질문(교수가 답변한 질문)
    user_question: str
    # STT로 변환된 텍스트
    stt_text: str


# STT 텍스트를 입력받아 정제된 질문과 LLM 답변을 반환하는 API
@router.post("/process_stt")
async def process_stt(input_data: STTInput):
    try:
        response = rag_pipeline(input_data.stt_text, input_data.user_question)
        return {
            "answer": response["LLMAnswer"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
