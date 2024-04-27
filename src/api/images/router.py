import hashlib
from typing import Any
from fastapi import Form, HTTPException, File, UploadFile, APIRouter, Response
from sqlalchemy.orm.exc import NoResultFound

from common.database.session import DatabaseSessionManager
from api.images.config import mime_type_mapping
from common.models.image import Image


images_router = APIRouter(prefix="/images", tags=["Images"])

@images_router.get("/{file_hash}")
async def get_image(file_hash: str):
    with DatabaseSessionManager() as session:
        try:
            # Извлекаем изображение из базы данных по ID
            image = session.query(Image).filter(Image.hash == file_hash).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image.data, media_type=image.content_type)

@images_router.post("/convert")
async def convert_image(file: UploadFile = File(Any), source_format: str = Form(Any), target_format: str = Form(Any)):
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

    hash_sha256 = hashlib.sha256()
    hash_sha256.update(file_content)
    file_hash = hash_sha256.hexdigest()

    new_image = Image(filename=file.filename, content_type=file.content_type, data=file_content, converted=False, hash=file_hash)
    with DatabaseSessionManager() as session:
        session.add(new_image)
        session.commit()

    return {"message": f"Received file {file.filename} with hash {file_hash } and content type {file.content_type}. Converting from {source_format} to {target_format}"}