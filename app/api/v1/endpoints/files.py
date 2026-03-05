from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from pathlib import Path
import shutil

# File - Читает весь файл в память (ОЗУ RAM оперативная память), не подходит для работы с большими файлами
# UploadedFile - потоковая загрузка, не грузит файлы в RAM, используется в production

router = APIRouter(prefix="/files", tags=["Работа с файлами"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"txt/plain", "application/pdf", "image/png", "image/jpeg"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Данный формат файлов не поддерживается")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}