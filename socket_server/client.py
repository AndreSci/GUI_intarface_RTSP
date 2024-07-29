import datetime
import random
import socket
import io
from PIL import Image, ImageSequence


# HOST = "192.168.15.10"  # The server's hostname or IP address
# PORT = 9099  # The port used by the server
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8080  # The port used by the server

NO_SIG_INDEX_FOR = {'CAM999': {'index': 1}}

GLOB_IMG_NO_SIGNAL = []


class GifToBytes:
    def __init__(self):
        """ Предварительно у нас 110 кадров """
        self.full_gif = Image.open('./gui/no-signal-stand-by.gif')

        self._rebuild_global()

    @staticmethod
    def get_img(index: int) -> bytes:
        if index > len(GLOB_IMG_NO_SIGNAL):
            raise IndexError(f"Исключение вызвало указание индекса больше чем доступно в массиве ")
        return GLOB_IMG_NO_SIGNAL[index]

    @staticmethod
    def get_size():
        return len(GLOB_IMG_NO_SIGNAL)

    def _rebuild_global(self):
        """ Заполняем глобальную переменную кадрами """
        global GLOB_IMG_NO_SIGNAL

        try:
            for image in ImageSequence.Iterator(self.full_gif):

                img_byte_arr = io.BytesIO()
                image.convert('RGB').save(img_byte_arr, format='JPEG')

                GLOB_IMG_NO_SIGNAL.append(img_byte_arr.getvalue())
        except Exception as ex:
            print(f"GifToBytes._rebuild_global: Исключение вызвало: {ex}")


class PairRetValue:

    def __init__(self):
        self.result = False
        self.byte_img = b''
        self.size = 0
        self.time_start = datetime.datetime.now()
        self.time_end = datetime.datetime.now()


class NoSigClass:
    @staticmethod
    def get_img(cam_name: str):
        global NO_SIG_INDEX_FOR

        if cam_name in NO_SIG_INDEX_FOR:
            NO_SIG_INDEX_FOR[cam_name]['index'] += 1
        else:
            NO_SIG_INDEX_FOR[cam_name] = {'index': 1}

        return GifToBytes.get_img(NO_SIG_INDEX_FOR[cam_name]['index'])


class ClientSocket:

    @staticmethod
    def take_frame(cam_num: str) -> PairRetValue:
        ret_value = PairRetValue()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((HOST, PORT))
                s.sendall(f"CAM{cam_num}".encode())

                len_data = s.recv(4)
                len_data = int.from_bytes(len_data, byteorder='big')
                # print(f"Длинна кадра: {int.from_bytes(len_data)}")

                ret_value.time_start = datetime.datetime.now()
                data_list = list()
                data1 = s.recv(len_data)
                data_list.append(data1)

                len_compare = len(data1)

                while len_compare < len_data:
                    data_w = s.recv(len_data - len_compare)
                    data_list.append(data_w)
                    len_compare = len_compare + len(data_w)

                ret_value.time_end = datetime.datetime.now()

                ret_value.byte_img = b''.join(data_list)
                ret_value.size = len(ret_value.byte_img)

        except Exception as ex:
            """ Не требуется описание ошибки, просто пропускаем и возвращаем пустой байт-код """

            ret_value.byte_img = NoSigClass.get_img(f"CAM{cam_num}")
            ret_value.time_end = datetime.datetime.now()

        if ret_value.size > 43351:
            ret_value.result = True

        return ret_value


if __name__ == "__main__":
    print(ClientSocket.take_frame("2"))
