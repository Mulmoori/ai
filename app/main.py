# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import stt_router, update_router, query_router
from app.services.chroma_client import get_chroma_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 코드
    chroma_client = get_chroma_client()
    print("🛠️ Chroma 클라이언트 초기화 완료")

    yield  # 앱이 실행되는 동안 유지됨

    # 애플리케이션 종료 시 실행될 코드
    print("✅ 애플리케이션 종료 중...")


app = FastAPI(lifespan=lifespan)

# STT 라우터 포함
app.include_router(stt_router.router)

# Query 라우터 포함
app.include_router(query_router.router)

# Vector store 업데이트 라우터 등록
app.include_router(update_router.router)
