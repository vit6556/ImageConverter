import random
import hashlib
from typing import Any
from fastapi import Form, HTTPException, File, UploadFile, APIRouter, Response
from sqlalchemy.orm.exc import NoResultFound

from api.images.config import mime_type_mapping
from api.images.schema import ImageFormat
from common.models.image import Image
from common.database.session import DatabaseSessionManager, redis_client
from api.images.utils import get_cache, set_cache


images_router = APIRouter(prefix="/images", tags=["Images"])

@images_router.get("/{file_hash}")
async def get_image(file_hash: str):
    with DatabaseSessionManager() as session:
        try:
            # Извлекаем изображение из базы данных по ID
            image = session.query(Image).filter(Image.hash == file_hash).filter(Image.converted == True).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image.data, media_type=mime_type_mapping[image.source_content_type])

@images_router.get("/status/{file_hash}")
async def get_convertion_status(file_hash: str):
    cache_key = f"item-{file_hash}"
    response = get_cache(cache_key)
    if response:
        response["from_cache"] = True
    else:
        with DatabaseSessionManager() as session:
            try:
                # Извлекаем изображение из базы данных по ID
                image = session.query(Image).filter(Image.hash == file_hash).filter(Image.converted == True).one()
                response = {"status": "Image converted", "download_url": images_router.url_path_for("get_image", file_hash=image.hash)}
            except NoResultFound:
                response = {"status": "Image not converted"}

        set_cache(cache_key, response)
        response["from_cache"] = False

    return response

@images_router.post("/convert")
async def convert_image(file: UploadFile = File(Any), source_format: ImageFormat = Form(Any), target_format: ImageFormat = Form(Any)):
    # Проверка MIME-типа файла
    if file.content_type not in mime_type_mapping.values():
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {file.content_type}")

    # Проверка соответствия выбранного формата и MIME-типа файла
    source_mime_type = mime_type_mapping.get(source_format)
    if file.content_type != source_mime_type:
        raise HTTPException(status_code=400, detail=f"The uploaded file type does not match the selected source format. Expected {source_mime_type}, got {file.content_type}")

    if source_format == target_format:
        raise HTTPException(status_code=400, detail="Source and target format cannot be the same.")

    if not target_format in mime_type_mapping.keys():
        raise HTTPException(status_code=400, detail="Unknown target format")

    file_content = await file.read()

    hash_sha256 = hashlib.sha256()
    hash_sha256.update(file_content + str(random.random()).encode())
    file_hash = hash_sha256.hexdigest()

    # Добавление изображения в бд
    new_image = Image(filename=file.filename, source_content_type=source_format, target_content_type=target_format, data=file_content, converted=False, hash=file_hash)
    with DatabaseSessionManager() as session:
        session.add(new_image)
        session.commit()

    # Добавление изображения в список задач
    redis_client.lpush('image_tasks', file_hash)

    return {"file_hash": file_hash}