# Dockerfile

# 베이스 이미지로 Python 3.11을 사용합니다.
FROM python:3.11-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 필요 패키지 설치를 위해 pip 업그레이드
RUN pip install --upgrade pip

# 로컬의 requirements.txt를 컨테이너로 복사합니다.
COPY requirements.txt .

# 필요한 파이썬 패키지를 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 파일들을 컨테이너로 복사합니다.
COPY . .

# 8000 포트를 외부에 노출합니다.
EXPOSE 8000

# Uvicorn 서버를 통해 FastAPI 애플리케이션을 실행합니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

