from PIL import Image
import io
from typing import Any
from misc.speed_test_decor import ShowWorkSpeed


class ChangeImg:
    @staticmethod
    @ShowWorkSpeed
    def resize(byte_img: bytes, new_size: Any) -> bytes:
        """ byte_img = b'',
        new_size = (800, 600) """
        # Создание объекта изображения из байт-кода
        image = Image.open(io.BytesIO(byte_img))

        # Изменение размера изображения
        resized_image = image.resize(new_size, Image.LANCZOS)

        # Сохранение измененного изображения обратно в байт-код
        output = io.BytesIO()
        resized_image.save(output, format=image.format)
        resized_byte_data = output.getvalue()

        # Теперь resized_byte_data содержит байт-код измененного изображения

        return resized_byte_data


if __name__ == "__main__":
    with open('../icon.png', 'rb') as file:

        print(len(ChangeImg.resize(file.read(), (400, 200))))
