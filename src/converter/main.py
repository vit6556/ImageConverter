import time

from converter.utils import convert_image
from common.models.image import Image
from common.database.session import redis_client, DatabaseSessionManager


def main():
    while True:
        _, image_hash = redis_client.blpop('image_tasks', timeout=0)

        with DatabaseSessionManager() as session:
            image = session.query(Image).filter(Image.hash == image_hash).one()
            converted_image = Image(filename=image.filename, source_content_type=image.source_content_type, target_content_type=image.target_content_type,
                              data=convert_image(image.data, image.target_content_type), hash=image.hash, converted=True)

            session.add(converted_image)
            session.commit()

        cache_key = f"item-{image_hash}"
        redis_client.delete(cache_key)

if __name__ == '__main__':
    main()