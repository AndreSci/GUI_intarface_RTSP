import time
from threading import Thread
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QPushButton
from socket_server.client import ClientSocket

TIME_FOR_UPDATE_BUTTON = 2


class Button(QPushButton):
    """ Заглушка для Typing """
    def __init__(self, num, text):  # !!!
        super().__init__()

        self.setText(f'{text}')  # !!! {text} {num}


class ButtonPic:
    """ Класс предназначен для обновления изображения на кнопках выбора камер """
    def __init__(self, sig_update, buttons: list, rtsp_host: str, rtsp_port: int, update_img: bool = False):
        self.update_img = update_img
        self.signal = sig_update
        self.list_button = buttons
        self.len_index_done = 0
        self.len_buttons = len(buttons)

        self.rtsp_host = rtsp_host
        self.rtsp_port = rtsp_port

        self.thread = Thread(target=self._update_buttons, daemon=True)
        self.thread.start()

    def _update_buttons(self):
        for but in self.list_button:
            thread = Thread(target=self._update_button, args=[but, ], daemon=True)
            thread.start()
            time.sleep(0.1)

    def _update_button(self, but: QtWidgets.QLabel):

        try:
            but_text = but.objectName()

            cam_number = but_text[3:len(but_text)]
            res_req = requests.get(f"http://{self.rtsp_host}:{self.rtsp_port}/action.do?video_in=CAM:{cam_number}",
                                   timeout=5)

            bytes_img = res_req.content

            self.signal.emit(bytes_img, but, self.update_img)
        except Exception as ex:
            print(f"Exception in: {ex}")
        finally:
            self.len_index_done += 1

    def check_end(self) -> bool:
        if self.len_buttons == self.len_index_done:
            return True
        else:
            return False
