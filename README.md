# Mulmoori

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Langchain](https://img.shields.io/badge/Langchain-7952B3?style=for-the-badge)](https://github.com/hwchase17/langchain)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## 🚀 Features# 설정

## 1. 가상 환경 생성

가상 환경을 생성하기 위해 아래 명령어를 실행합니다.

```sh
python -m venv ./env
```

## 2. 가상 환경 실행

가상 환경을 활성화하기 위해 아래 명령어를 실행합니다.

```sh
source env/bin/activate
```

## 3. 사전정의 패키지 구성 적용

필요한 패키지를 설치하기 위해 아래 명령어를 실행합니다.

```sh
pip install -r requirements.txt
```

## 4. 환경변수 설정

`.env` 파일을 생성하고 아래 내용을 추가합니다.

```sh
DATABASE_URL="<데이터베이스 URL>"
OPENAI_API_KEY="<OpenAI API Key>"
```

# 실행 가이드

## 1. fastAPI 실행

FastAPI 서버를 실행하기 위해 아래 명령어를 실행합니다.

```sh
uvicorn app.main:app --reload
```

-   실행 전 IDE 재부팅 권장
