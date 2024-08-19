# app/services/llm_service.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 언어 모델 초기화
print("🔧 언어 모델 초기화 중...")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# 프롬프트 템플릿 생성
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
            당신은 AI 어시스턴트입니다. 주어진 질문이 STT(음성 인식)로 변환된 텍스트라서 언어가 섞이거나 오타가 있을 수 있습니다.
            사용자가 입력한 질문을 정제하고, 정제된 질문을 바탕으로 명확한 답변을 제공하세요.
            
            교수가 답변한 원본 질문 : {original_question}
            
            교수가 답변한 원본 답변: {user_question}
            
            교수가 답변한 원본 질문-답변에 기반하여 명확하고 간결한 답변을 제공하세요.
            """
        ),
        HumanMessagePromptTemplate.from_template("{user_question}"),
    ]
)


def rag_pipeline(stt_input: str, user_question: str) -> dict:
    # STT 입력 텍스트 정제
    stt_input

    # LLM에 정제된 질문 전달
    print("💬 LLM을 통한 답변 생성 중...")
    prompt = prompt_template.format(
        original_question=stt_input, user_question=user_question
    )
    output = llm.invoke(prompt)

    return {"LLMAnswer": output.content, "userQuestion": user_question}
