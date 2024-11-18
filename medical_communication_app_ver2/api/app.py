from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.main import main
from app.rag_agent import RAGAgent
from app.database import init_db
from pathlib import Path
import threading
import json

app = FastAPI()

# 데이터베이스 초기화
init_db()

# Static 및 Template 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 상태 변수 (Thread-safe)
status = {"state": "idle", "message": "", "result_file": None}
status_lock = threading.Lock()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # 업로드된 파일 저장
        upload_dir = Path("uploaded_files")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_location = upload_dir / file.filename
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # 상태 초기화
        with status_lock:
            status["state"] = "processing"
            status["message"] = "분석 중입니다..."
            status["result_file"] = None

        # 백그라운드 작업 실행
        background_tasks.add_task(process_file, file_location)

        return templates.TemplateResponse("processing.html", {"request": request})
    except Exception as e:
        with status_lock:
            status["state"] = "error"
            status["message"] = f"오류 발생: {str(e)}"
        return templates.TemplateResponse("error.html", {"request": request, "error_message": str(e)})

@app.get("/result/", response_class=HTMLResponse)
async def result_page(request: Request):
    result_files = list(Path("output").glob("*_analyzed.json"))
    if not result_files:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_message": "분석된 파일을 찾을 수 없습니다."},
        )

    # 가장 최근의 결과 파일 선택
    result_path = max(result_files, key=lambda x: x.stat().st_mtime)

    # 결과 파일에서 분석된 데이터를 추출
    with open(result_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        analysis_result = data.get("analysis", {})
        if not isinstance(analysis_result, dict):
            # 분석 결과가 딕셔너리가 아닌 경우 처리
            analysis_result = {"전체응답": str(analysis_result)}

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "analysis_result": analysis_result,
        },
    )

from fastapi.responses import FileResponse

@app.get("/download/", response_class=FileResponse)
async def download_result():
    result_files = list(Path("output").glob("*_analyzed.json"))
    if not result_files:
        return JSONResponse(status_code=404, content={"message": "분석된 파일을 찾을 수 없습니다."})

    # 가장 최근의 결과 파일 선택
    result_path = max(result_files, key=lambda x: x.stat().st_mtime)

    return FileResponse(
        path=result_path,
        filename="analysis_result.json",
        media_type="application/json"
    )


from fastapi.responses import JSONResponse

@app.get("/status/", response_class=JSONResponse)
async def get_status():
    global status
    with status_lock:
        return {
            "state": status["state"],
            "message": status["message"],
            "result_file": status["result_file"],
        }
    
@app.get("/error/", response_class=HTMLResponse)
async def error_page(request: Request):
    global status
    with status_lock:
        error_message = status.get("message", "알 수 없는 오류가 발생했습니다.")
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error_message": error_message},
    )

def process_file(file_location: Path):
    global status
    try:
        # STT 및 화자 분리 실행
        with status_lock:
            status["message"] = "음성 변환 및 화자 분리 중..."
        intermediate_result_path = main(file_location)

        # 대화 내용 추출
        with open(intermediate_result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        conversation_text = data.get("transcription_text", "")

        # RAG 에이전트 사용하여 분석 실행
        with status_lock:
            status["message"] = "LLM 분석 중..."
        rag_agent = RAGAgent()
        analysis_result = rag_agent.generate_response(conversation_text)

        # 결과 저장
        data["analysis"] = analysis_result
        final_result_path = intermediate_result_path.parent / f"{intermediate_result_path.stem}_analyzed.json"
        with open(final_result_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 상태 완료로 업데이트
        with status_lock:
            status["state"] = "completed"
            status["message"] = "분석 완료. 결과를 확인하세요."
            status["result_file"] = final_result_path.name

    except Exception as e:
        # 에러 로그 출력
        print(f"LLM 분석 중 오류 발생: {e}")
        with status_lock:
            status["state"] = "error"
            status["message"] = f"오류 발생: {str(e)}"