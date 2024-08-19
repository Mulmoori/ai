# app/models/request_models.py

from pydantic import BaseModel


# 쿼리 요청 모델
class QueryRequest(BaseModel):
    id: int  # 벡터 스토어의 ID
    question: str  # 사용자의 질문


# 벡터 스토어 업데이트 요청 모델
class UpdateVectorStoreRequest(BaseModel):
    id: int  # 벡터 스토어의 ID
    question: str  # 추가할 질문 목록
    answer: str  # 추가할 답변 목록
