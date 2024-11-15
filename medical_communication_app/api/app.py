from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.main import main
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = Path("data") / file.filename
    with open(file_location, "wb") as f:
        f.write(await file.read())
    main()
    result_path = Path("output") / "result.json"
    return templates.TemplateResponse("result.html", {"request": {}, "result_file": result_path})