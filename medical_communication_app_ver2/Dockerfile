# Python 기반 이미지
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 복사
COPY requirements.txt /app/

# 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY . /app/

# 포트 노출
EXPOSE 8000

# FastAPI 실행
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]