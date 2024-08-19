# app/services/chroma_client.py

from chromadb import Client as ChromaClient
from chromadb.config import Settings

# 전역적으로 한 번만 Chroma 클라이언트를 초기화
_chroma_client = None


def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = ChromaClient(Settings(persist_directory="./chroma_data"))
    return _chroma_client
