import datetime
import threading
import time
import requests

from PyQt5 import QtCore, QtGui, QtWidgets, Qt, QtNetwork
from PyQt5.Qt import QPushButton
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap

from gui.camera_gui import Ui_MainWindow
from enum import Enum
from socket_server.client import ClientSocket, GifToBytes
from requests_to_rtsp.connection import CamerasRTPS
from windows.button_cams import ButtonPic

from misc.resize_img import ChangeImg
from misc.logger import Logger
from misc.globals_value import GlobControlCamerasList, GlobalControl
from misc.read_data import TypeBarrierStatus, ReadCode
from misc.globals_value import (NAME_VER, TIME_CHECK_STATUS, BARRIER_FID)


class ActionType(Enum):
    """ Служит для определения статуса действий """
    opened = 1
    closed = 2
    wait = 3


class MainClassTitle(QtWidgets.QMainWindow):
    """ Базовый класс """
    def __init__(self):
        super().__init__()
        # Объявляем интерфейс
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(NAME_VER)


class ControlClassElements(MainClassTitle):
    """ Класс для общих элементов интерфейса """
    signal_status = QtCore.pyqtSignal(ActionType)
    signal_change_img = QtCore.pyqtSignal(bytes)
    signal_update_cams = QtCore.pyqtSignal()
    signal_update_button = QtCore.pyqtSignal(bytes, QtWidgets.QLabel, bool)
    signal_change_warning_msg = QtCore.pyqtSignal(str)
    signal_gate_state_img = QtCore.pyqtSignal(str)

    def __init__(self, common_host: str, common_port: int):
        super().__init__()
        self.host = common_host
        self.port = common_port
        self.camera_number = '07'
        self.window_number = 3


class GateStateClass(ControlClassElements):
    """ Класс отвечает за обновление блока кнопок камер """
    def __init__(self, host, port):
        super().__init__(host, port)

        self.signal_gate_state_img.connect(self.__change_img_state)

        tr_gate_img = threading.Thread(target=self.__while_gate_img, daemon=True)
        tr_gate_img.start()

    def __while_gate_img(self):
        """ Отвечает за получение статуса проезда и отсылает команду на обновление картинки """
        while True:
            time.sleep(0.1)
            self.signal_gate_state_img.emit('./gui/gates/no_signal.jpg')

    def __change_img_state(self, url_file: str):
        """ Отвечает за смену картинки с изображением проезда """
        pixmap = QPixmap()
        pixmap.load(url_file)
        pixmap.scaled(400, 300)

        self.ui.gate_state_3.setPixmap(QtGui.QPixmap(pixmap))


class ButtonClass(GateStateClass):
    """ Класс отвечает за обновление блока кнопок камер """
    def __init__(self, host, port):
        super().__init__(host, port)
        self.request_update_buttons = False
        # QWidget
        self.list_widgets = list()

        self.ui.but_update_cams.clicked.connect(self.__update_buttons_for_cams)

        self.tr_buttons_cam = threading.Thread(target=self.__while_update_buttons, daemon=True)
        self.tr_buttons_cam.start()

        self.signal_update_cams.connect(self.__update_buttons_for_cams)
        self.signal_update_button.connect(self.__update_button_img)

    def __update_buttons_for_cams(self):
        """ Обновляем список камер и пересоздает все кнопки связанные с выбором камеры """

        if not self.request_update_buttons:
            self.request_update_buttons = True
            self.ui.warning_msg.setText(f"Ожидаем обновление кнопок.")

    def __while_update_buttons(self):
        """ Функция обновления списка кнопок по триггеру (Запускается в отдельном потоке)"""
        while True:
            if self.request_update_buttons:
                try:
                    GlobControlCamerasList.update(CamerasRTPS.get_list(self.host,
                                                                       self.port,
                                                                       'admin',
                                                                       'admin'))

                    self.__create_buttons()

                    self.signal_change_warning_msg.emit("Обновление кнопок камер завершено.")
                except Exception as ex:
                    print(f"Exception in __while_update_buttons: {ex}")
                    self.signal_change_warning_msg.emit("Не удалось обновить кнопки камер.")
                finally:
                    self.request_update_buttons = False

            else:
                time.sleep(1)

    def __create_buttons(self):
        """ Пересоздает все кнопки связанные с выбором камеры """
        step = 0

        if self.list_widgets:
            for widget in self.list_widgets:
                widget.setParent(None)
                widget.destroy()
                # self.ui.verticalLayout_4.removeWidget(widget)

            self.list_widgets = list()

        for data in GlobControlCamerasList.get_list():
            cam_name = data.get('FName')
            step += 1
            self.__add_label(cam_name, step)

    def __add_label(self, cam_name: str, index: int):
        label_cam = QtWidgets.QLabel()   # self.ui.scrollAreaWidgetContents_2)
        label_cam.setMinimumSize(QtCore.QSize(120, 68))
        label_cam.setMaximumSize(QtCore.QSize(120, 100))
        label_cam.setStyleSheet("color: rgb(50, 50, 50); border: 1px solid; border-color: rgb(0,0,0);")
        label_cam.setObjectName(f"{cam_name}")
        label_cam.setText(cam_name)
        label_cam.setAlignment(Qt.Qt.AlignCenter)
        label_cam.mousePressEvent = (lambda ch, b=label_cam: self.chosen_camera_button(b))

        self.ui.verticalLayout_4.addWidget(label_cam)

        self.list_widgets.append(label_cam)

    def chosen_camera_button(self, btn: QtWidgets.QLabel):
        """ Тупо меняет переменную в классе которая отвечает за номер камеры в запросе,
        получаем данные из имени кнопки """

        name = btn.objectName()
        self.ui.lab_cam_name.setText(f"Просмотр камеры: {name}")
        self.ui.Frame_Gate_For_Hide.hide()
        self.camera_number = name[3:len(name)]

    @staticmethod
    def __update_button_img(byte_img: bytes, btn: QtWidgets.QLabel, update_img: bool = False):
        """ Функция обновляет картинку в кнопке """
        if update_img:
            pixmap = QPixmap()
            pixmap.loadFromData(byte_img)
            size_but = btn.size()
            pixmap = pixmap.scaled(size_but.width(), size_but.height())

            btn.setPixmap(pixmap)
        else:
            btn.setText(btn.objectName())


class MainClass(ButtonClass):
    """ Класс для конечного наследования """
    def __init__(self, host, port):
        super().__init__(host, port)

        pass
