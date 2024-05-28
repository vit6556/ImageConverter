import os
import io
import sys
import time
from PIL import Image as PImage
from sqlalchemy.orm import Session

python_path = os.path.join(os.getcwd())
sys.path.append(python_path)
os.environ["PYTHONPATH"] = python_path

from common.models.image import Image
from common.database.session import redis_client, DatabaseSessionManager


def convert_image(input_image_bytes: bytes, output_format: str):
    """ Конвертирует изображение из одного формата в другой и возвращает байты результата """
    input_image = PImage.open(io.BytesIO(input_image_bytes))

    # Если конвертация в 'jpg' или 'jpeg' и исходное изображение имеет альфа-канал
    if (output_format in ['jpg', 'jpeg']) and input_image.mode in ['RGBA', 'LA']:
        # Создание белого фона для замены прозрачных участков
        background = PImage.new("RGB", input_image.size, (255, 255, 255))
        background.paste(input_image, mask=input_image.split()[3])  # 3 - альфа-канал
        output_image = background
    else:
        output_image = input_image.convert("RGB")

    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format=output_format.upper())

    return img_byte_arr.getvalue()


def main():
    while True:
        _, image_hash = redis_client.blpop('image_tasks', timeout=0)

        with DatabaseSessionManager() as session:
            image = session.query(Image).filter(Image.hash == image_hash).one()
            new_image = Image(filename=image.filename, source_content_type=image.source_content_type, target_content_type=image.target_content_type,
                              data=convert_image(image.data, image.target_content_type), hash=image.hash, converted=True)

            session.add(new_image)
            session.commit()

        time.sleep(0.1)

if __name__ == '__main__':
    main()