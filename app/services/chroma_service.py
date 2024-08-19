# app/services/chroma_service.py
import uuid
from chromadb.config import Settings
import os
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from chromadb import Client as ChromaClient
from langchain_openai import OpenAIEmbeddings

# 언어 모델 초기화
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# OpenAI 임베딩 모델 초기화
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")


# 프롬프트 템플릿 생성
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
            당신은 AI 어시스턴트입니다. 
            사용자가 질문에 대한 답변을 찾을 수 있도록 돕습니다.
            
            사용자 질문과 유사한 질의응답 선례 : {context}

            위 선례에 기반하여 사용자의 질문에 대한 답변을 친절하게 설명해주세요.
            """
        ),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)


def load_vectorstore(id: str):
    # Chroma 벡터 스토어 클라이언트 초기화
    client = ChromaClient()

    # ID에 해당하는 벡터 스토어 로드
    vectorstore = client.get_collection(name=id, embedding_function=embedding_model)

    return vectorstore


def query_vectorstore(vectorstore, question: str):
    # 질문을 벡터(임베딩)로 변환
    question_embedding = embedding_model.embed_documents([question])[
        0
    ]  # 벡터 리스트로 변환

    print("임베딩된 질문:", question_embedding)

    # 벡터 스토어에서 질문에 가장 유사한 문서를 검색
    results = vectorstore.query(
        query_texts=[question], n_results=1  # 직접 검색할 쿼리 텍스트를 전달
    )

    print("검색 결과:", results)

    # 필요한 형태로 결과 처리
    # 필요한 형태로 결과 처리
    if results and len(results["metadatas"]) > 0:
        most_similar_metadata = results["metadatas"][0][
            0
        ]  # 첫 번째 결과의 메타데이터 가져오기
        answer = most_similar_metadata.get("answer", "답변을 찾을 수 없습니다.")
        print("가장 유사한 답변:", answer)
        return answer
    else:
        return "관련된 문서를 찾을 수 없습니다."


class LangchainEmbeddingFunction:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def __call__(self, input):
        return self.embedding_model.embed_documents(input)


def load_or_create_vectorstore(id: str, client: ChromaClient):
    print("🔧 벡터 스토어 초기화 중...")

    # ID를 문자열로 변환하고, Chroma의 컬렉션 이름 요구사항을 충족하도록 조정
    id_str = f"collection_{id}"  # 예: "1" -> "collection_001"

    # 새로운 래퍼 클래스 인스턴스를 생성
    embedding_function = LangchainEmbeddingFunction(embedding_model)

    try:
        # 이미 존재하는 컬렉션을 로드
        print("벡터 스토어 로드 중...")
        vectorstore = client.get_collection(
            name=id_str,
            embedding_function=embedding_function,  # 래핑된 임베딩 함수 사용
        )
        print("벡터 스토어 로드 완료")
    except Exception as e:
        # 벡터 스토어가 없으면 생성
        print(f"벡터 스토어 로드 실패, 새로 생성: {e}")
        vectorstore = client.create_collection(
            name=id_str,
            embedding_function=embedding_function,  # 래핑된 임베딩 함수 사용
        )
        print("새 벡터 스토어 생성 완료")

    return vectorstore


# app/services/chroma_service.py


def append_to_vectorstore(vectorstore, question: str, answer: str):
    # 단일 문자열이므로 리스트로 변환
    questions = [question]
    answers = [answer]

    # 질문을 기반으로 임베딩 생성 및 벡터 스토어에 추가
    for question, answer in zip(questions, answers):
        # OpenAI 임베딩 생성
        question_embedding = embedding_model.embed_documents([question])[0]

        # 벡터 스토어에 질문 및 답변 추가
        vectorstore.add(
            embeddings=[question_embedding],  # embeddings로 전달
            metadatas=[{"question": question, "answer": answer}],  # 리스트 형태로 전달
            ids=[str(uuid.uuid4())],  # 고유 ID 생성
        )
        print("벡터 스토어에 추가 완료")
