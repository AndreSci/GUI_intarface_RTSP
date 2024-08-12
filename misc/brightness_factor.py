""" Модуль отвечает за увеличение яркости картинки - (добавлен как визуал для кнопки 'Снимок'\'Screenshot') """
from PIL import Image
from io import BytesIO
import numpy as np


def increase_brightness(image_bytes, brightness_factor, image_format='JPEG'):
    # Открываем изображение из байтов
    img = Image.open(BytesIO(image_bytes))

    # Преобразуем изображение в массив numpy для удобства обработки
    img_array = np.array(img, dtype=np.float32)

    # Увеличиваем яркость на 50%
    img_array = img_array * brightness_factor

    # Ограничиваем значения пикселей в диапазоне от 0 до 255
    img_array = np.clip(img_array, 0, 255)

    # Преобразуем массив обратно в изображение
    img = Image.fromarray(img_array.astype(np.uint8))

    # Сохраняем изображение обратно в байты с указанием формата
    output_buffer = BytesIO()
    img.save(output_buffer, format=image_format)
    return output_buffer.getvalue()


def test_bright():
    # Пример использования
    with open("input_image.png", "rb") as f:
        image_bytes = f.read()

    # Увеличиваем яркость на 50%
    bright_image_bytes = increase_brightness(image_bytes, 1.5)

    # Сохраняем результат для проверки
    with open("output_image.png", "wb") as f:
        f.write(bright_image_bytes)
