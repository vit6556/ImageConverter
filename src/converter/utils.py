import io
from PIL import Image


def convert_image(input_image_bytes: bytes, output_format: str):
    """ Конвертирует изображение из одного формата в другой и возвращает байты результата """
    input_image = Image.open(io.BytesIO(input_image_bytes))

    # Если конвертация в 'jpg' или 'jpeg' и исходное изображение имеет альфа-канал
    if (output_format in ['jpg', 'jpeg']) and input_image.mode in ['RGBA', 'LA']:
        # Создание белого фона для замены прозрачных участков
        background = Image.new("RGB", input_image.size, (255, 255, 255))
        background.paste(input_image, mask=input_image.split()[3])  # 3 - альфа-канал
        output_image = background
    else:
        output_image = input_image.convert("RGB")

    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format=output_format.upper())

    return img_byte_arr.getvalue()