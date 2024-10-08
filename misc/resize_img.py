from PIL import Image
import io
from datetime import datetime
from typing import Any
from misc.speed_test_decor import ShowWorkSpeed


class ChangeImg:
    @staticmethod
    def resize(byte_img: bytes, window_width, window_height) -> bytes:
        """ byte_img = b'',
        new_size = (800, 600) """
        try:
            # Создание объекта изображения из байт-кода
            image = Image.open(io.BytesIO(byte_img))

            scale_width = window_width / image.width
            scale_height = window_height / image.height

            if scale_height > scale_width:
                new_width = image.width * scale_width
                new_height = image.height * scale_width
            else:
                new_width = image.width * scale_height
                new_height = image.height * scale_height

            # Изменение размера изображения
            resized_image = image.resize((int(new_width), int(new_height)), Image.LANCZOS)

            # Сохранение измененного изображения обратно в байт-код
            output = io.BytesIO()
            resized_image.save(output, format=image.format, quality=95)
            resized_byte_data = output.getvalue()

            # Теперь resized_byte_data содержит байт-код измененного изображения
        except Exception as ex:
            print(f"Exception in {ex}")
            resized_byte_data = b''

        # return resized_byte_data
        return resized_byte_data

    @staticmethod
    def save_screenshot(byte_img: bytes, cam_number: str):
        try:
            # Открываем изображение с помощью Pillow
            with open(f"./screenshots/screen_{cam_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", 'wb') as f:
                f.write(byte_img)

        except Exception as ex:
            print(f"Exception in screenshots creator: {ex}")


if __name__ == "__main__":
    with open('../icon.png', 'rb') as file:

        print(len(ChangeImg.resize(file.read(), 400, 200)))
