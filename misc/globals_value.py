import datetime
from collections import deque

RTSP_URL = '127.0.0.1'
RTSP_PORT = 8011
SOCKET_PORT = 9098

LIST_CAMERAS = [{'FName': 'NoConnection'}]

CON_INDEX = 0
CONNECTION_SPEED = deque()  # kbyte
MIN_CON_SPEED = 1500000  # byte need for update buttons img

NAME_VER = "VIG Camera Watcher + Gates Control"
TIME_CHECK_STATUS = 50  # ms.
BARRIER_FID = 2

NEW_IMG_SIZE_WEIGHT = 550
NEW_IMG_SIZE_HEIGHT = 350

HOST_RTSP = '127.0.0.1'
PORT_RTSP = 8011


class GlobControlCamerasList:
    @staticmethod
    def update(values: dict) -> list:
        global LIST_CAMERAS
        ret_value = list()

        ret_value.append({'FName': 'NoConnection'})

        for it in values:
            ret_value.append(it)
            # ret_value.append(str(it.get('FName')))

        if len(ret_value) > 1:
            LIST_CAMERAS = ret_value

        return ret_value

    @staticmethod
    def get_list() -> list:
        return LIST_CAMERAS


class GlobalControl:

    @staticmethod
    def test_speed(size_img: int, time_start: datetime.datetime, time_end: datetime.datetime) -> bool:
        """ Функция проверяет скорость скачивания кадров с RTSP сервера """
        # Метод нужен для снижения нагрузки на связь,
        # убирает получение кадров для кнопок выбора камер если низкая скорость связи
        global CONNECTION_SPEED, CON_INDEX, MIN_CON_SPEED

        try:
            delta_res = (time_end - time_start).total_seconds()

            if delta_res > 0:
                new_speed = (1 / delta_res) * size_img
            else:
                return True

            CONNECTION_SPEED.append(new_speed)

            if len(CONNECTION_SPEED) > 10:
                CONNECTION_SPEED.popleft()

            sum_num = 0
            for it in CONNECTION_SPEED:
                sum_num += it

            current_speed = sum_num / len(CONNECTION_SPEED)

            if current_speed > MIN_CON_SPEED and len(CONNECTION_SPEED) > 9:
                print(f"Скорость загрузки: {current_speed}")
                return True
            else:
                print(f"Скорость загрузки: {current_speed}")
                return False
        except Exception as ex:
            print(f"Исключение в работе проверки скорости соединения: {ex}")

        return False
