from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.stt_processor import STTProcessor
from app.rag_agent import RAGAgent
from app.database import init_db
from pathlib import Path
import threading
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

stt_processor = STTProcessor()
rag_agent = RAGAgent()
init_db()

status = {"state": "idle", "message": "", "result_file": ""}
status_lock = threading.Lock()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def process_audio(request: Request, file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    audio_path = f"uploads/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    def background_task():
        with status_lock:
            status["state"] = "processing"
            status["message"] = "오디오 파일을 처리 중입니다."
            status["result_file"] = ""

        try:
            # STT 처리
            transcription_file = stt_processor.process_audio(audio_path)
            with open(transcription_file, "r", encoding="utf-8") as f:
                transcription_data = json.load(f)
                conversation_text = "\n".join(
                    [f"{seg['speaker']}: {seg['text']}" for seg in transcription_data["segments"]]
                )

            # RAG 에이전트를 사용하여 분석
            analysis_result = rag_agent.generate_response(conversation_text)

            # 결과 저장
            os.makedirs("output", exist_ok=True)
            result_file = Path("output") / (Path(audio_path).stem + "_analyzed.json")
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump({"analysis": analysis_result}, f, ensure_ascii=False, indent=4)

            with status_lock:
                status["state"] = "completed"
                status["message"] = "분석이 완료되었습니다."
                status["result_file"] = str(result_file)

        except Exception as e:
            with status_lock:
                status["state"] = "error"
                status["message"] = f"오류 발생: {str(e)}"
                status["result_file"] = ""

    threading.Thread(target=background_task).start()

    return templates.TemplateResponse("processing.html", {"request": request})

@app.get("/status/", response_class=JSONResponse)
async def get_status():
    with status_lock:
        return status.copy()

@app.get("/result/", response_class=HTMLResponse)
async def result_page(request: Request):
    result_file = status.get("result_file", "")
    if not result_file:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "분석 결과를 찾을 수 없습니다."})

    with open(result_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        analysis_result = data.get("analysis", {})

    return templates.TemplateResponse("result.html", {"request": request, "analysis_result": analysis_result})

@app.get("/download/", response_class=FileResponse)
async def download_result():
    result_file = status.get("result_file", "")
    if not result_file:
        return JSONResponse(status_code=404, content={"message": "분석 결과를 찾을 수 없습니다."})

    return FileResponse(path=result_file, filename="analysis_result.json", media_type="application/json")

@app.get("/error/", response_class=HTMLResponse)
async def error_page(request: Request):
    error_message = status.get("message", "알 수 없는 오류가 발생했습니다.")
    return templates.TemplateResponse("error.html", {"request": request, "error_message": error_message})