from fastapi import Form, HTTPException, File, UploadFile, APIRouter
from typing import Any


images_router = APIRouter(prefix="/images", tags=["Images"])

@images_router.post("/convert")
async def convert_image(file: UploadFile = File(Any), source_format: str = Form(Any), target_format: str = Form(Any)):
    # Соответствие MIME-типов и расширений файлов
    mime_type_mapping = {
        "jpg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "bmp": "image/bmp"
    }

    # Проверка MIME-типа файла
    if file.content_type not in mime_type_mapping.values():
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {file.content_type}")

    # Проверка соответствия выбранного формата и MIME-типа файла
    expected_mime_type = mime_type_mapping.get(source_format)
    if file.content_type != expected_mime_type:
        raise HTTPException(status_code=400, detail=f"The uploaded file type does not match the selected source format. Expected {expected_mime_type}, got {file.content_type}")

    if source_format == target_format:
        raise HTTPException(status_code=400, detail="Source and target format cannot be the same.")

    file_content = await file.read()
    return {"message": f"Received file {file.filename} with content type {file.content_type} and converting from {source_format} to {target_format}"}