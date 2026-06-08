from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid

app = FastAPI()

# Создаем папку uploads, если ее нет
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Делаем папку доступной по ссылке
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def home():
    return {"message": "Saga Server is Live on Render!"}

@app.post("/upload-image")
async def upload_image(request: Request, file: UploadFile = File(...)):
    ext = Path(file.filename).suffix if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Сервер сам узнает свой URL (например, https://saga-backend...onrender.com)
    base_url = str(request.base_url).rstrip("/")
    
    return {
        "success": True,
        "filename": filename,
        "url": f"{base_url}/uploads/{filename}"
    }

@app.post("/upload-audio")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    ext = Path(file.filename).suffix if file.filename else ".m4a"
    filename = f"voice_{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    base_url = str(request.base_url).rstrip("/")
    
    return {
        "success": True,
        "filename": filename,
        "url": f"{base_url}/uploads/{filename}"
    }
