import datetime
import threading
import time
import json
import requests

from windows.class_main import MainClass, ActionType

from PyQt5 import QtCore, QtGui, QtWidgets, Qt, QtNetwork
from PyQt5.Qt import QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, QTimer, QByteArray
from PyQt5.QtCore import QSettings, QPoint, QSize
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QScrollArea, QVBoxLayout, QWidget

from gui.test_gui import Ui_MainWindow
from enum import Enum
from socket_server.client import ClientSocket, GifToBytes
from requests_to_rtsp.connection import CamerasRTPS, PairRetValue
from windows.button_cams import ButtonPic

from misc.resize_img import ChangeImg
from misc.logger import Logger
from windows.image_control import ControlUseImg
from misc.globals_value import GlobControlCamerasList, GlobalControl
from misc.read_data import TypeBarrierStatus, ReadCode
from misc.globals_value import (NAME_VER, TIME_CHECK_STATUS, BARRIER_FID)


logger = Logger()


class ThreadImgControl(QThread):
    """ Класс поток отвечает за обновление кадров в окне """
    change_img = pyqtSignal()

    def run(self):
        while True:
            QThread.msleep(200)
            self.change_img.emit()


class MainWindow(QtWidgets.QMainWindow):
    signal_update_buttons = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Настройки связи
        self.host = "192.168.15.10"
        self.port = 8093
        # Восстанавливаем сохраненные параметры окна
        self.settings = QSettings("VIG_TECH", "GUI_GATE_CONTROL")
        self.restore_window_state()

        # Настраиваем положение окон отображения изображения
        self.ui.horizontalLayout_5.setStretch(0, 1)
        self.ui.horizontalLayout_5.setStretch(1, 1)

        # self.ui.verticalLayout_2.addStretch()

        # Создание новых кнопок для камер
        self.camera_list = list()
        self.list_widgets = list()
        self.container_widget = QWidget()
        self.stretch_index = 0

        # Управление выбором камеры
        self.chosen_camera = 'CAM0'

        self.img_cont = ControlUseImg()
        self.gate_position = 9
        self.object_in = 6

        self.qtr1 = ThreadImgControl()
        self.qtr1.change_img.connect(self.__while_img)
        self.qtr1.start()
        # tr1 = threading.Thread(target=self.__while_img, daemon=True)
        # tr1.start()

        # Отвечает за смену изображения в разделе для камеры и для статуса проезда
        # Загружаем GIF с помощью QMovie
        self.movie = QMovie("./gui/no-signal-stand-by.gif")
        self.switch_movie = True
        # self.label.setMovie(self.movie)

        self.last_gate_img = b''
        self.last_video_img = b''

        self.resize_video_img = b''
        self.new_video_img = True
        self.time_new_video_img = datetime.datetime.now()

        self.size_video_wight = 1
        self.size_video_height = 1

        # Зона показать спрятать управление проездом
        self.show_gate_state = True

        with open("./test_img.jpg", 'rb') as file:
            self.last_video_img = file.read()

        tr2 = threading.Thread(target=self.__while_test_change_pos, daemon=True)
        tr2.start()

        tr_buttons = threading.Thread(target=self.__while_update_buttons, daemon=True)
        tr_buttons.start()

        tr_video = threading.Thread(target=self.__rtsp_http_get, daemon=True)
        tr_video.start()

        self.ui.video_img.mousePressEvent = (lambda ch, b='0': self.__show_hide_gate_control())

        self.signal_update_buttons.connect(self.__create_buttons)

        # Кнопки
        self.ui.screen_shot.clicked.connect(self.do_screenshot)

    def __while_test_change_pos(self):

        object_in_bool = True

        while True:
            time.sleep(1)
            # старт въезд
            self.gate_position = 9
            self.object_in = 6
            time.sleep(1)
            self.gate_position = 10
            self.object_in = 6
            time.sleep(1)
            # Открыт
            self.gate_position = 8
            self.object_in = 6
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 2
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 1
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 3
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 5
            time.sleep(1)
            self.gate_position = 8
            self.object_in = 0
            time.sleep(1)
            self.gate_position = 10
            self.object_in = 0
            time.sleep(1)
            # Конец закрыто
            self.gate_position = 9
            self.object_in = 0

            time.sleep(4)
            # ------------------------------
            # старт въезд
            self.gate_position = 9
            self.object_in = 5
            time.sleep(1)
            self.gate_position = 10
            self.object_in = 5
            time.sleep(1)
            # Открыт
            self.gate_position = 8
            self.object_in = 5
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 3
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 1
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 2
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 6
            time.sleep(0.5)
            self.gate_position = 8
            self.object_in = 0
            time.sleep(1)
            self.gate_position = 10
            self.object_in = 0
            time.sleep(1)
            # Конец закрыто
            self.gate_position = 9
            self.object_in = 0

            time.sleep(4)

            if object_in_bool:
                object_in_bool = False
                self.gate_position = 9
                self.object_in = 4
                time.sleep(2)
                self.gate_position = 8
                self.object_in = 4
                time.sleep(2)
            else:
                object_in_bool = True

    def __rtsp_http_get(self):
        """ Отвечает за получение кадров из RTSP сервера по имени камеры"""

        while True:
            frame_res = CamerasRTPS.get_frame(self.host, self.port, self.chosen_camera)

            if frame_res.result:
                self.new_video_img = True
                self.time_new_video_img = datetime.datetime.now()
                self.last_video_img = frame_res.byte_img

    def __while_img(self):
        self.__change_main_img(self.img_cont.get_img(self.gate_position, self.object_in))

    def __change_main_img(self, byte_img: bytes) -> None:
        """ Вызывается через сигнал и меняет изображение в главном секторе для отображения камеры """

        window_width = self.ui.gate_img.width()
        window_height = self.ui.gate_img.height()

        # Меняем размер нужного кадра
        byte_img = ChangeImg.resize(byte_img, window_width, window_height)

        pixmap = QPixmap()
        pixmap.loadFromData(byte_img)
        # self.ui.lab_camera_img.setPixmap(QtGui.QPixmap(pixmap))
        self.ui.gate_img.setPixmap(QtGui.QPixmap(pixmap))

        # ==================================================================
        new_window_width = self.ui.video_img.width()
        new_window_height = self.ui.video_img.height()

        if (datetime.datetime.now() - self.time_new_video_img).total_seconds() > 5:
            if self.switch_movie:
                # Включаем масштабирование содержимого
                self.ui.video_img.setScaledContents(True)
                self.ui.video_img.setMovie(self.movie)
                self.switch_movie = False
                # Запускаем анимацию
                self.movie.start()
        else:
            if (self.size_video_height != new_window_height
                    or self.size_video_wight != new_window_width
                    or self.new_video_img):
                self.new_video_img = False

                self.size_video_height = new_window_height
                self.size_video_wight = new_window_width
                self.resize_video_img = ChangeImg.resize(self.last_video_img, new_window_width, new_window_height)

            self.switch_movie = True
            self.movie.stop()
            self.ui.video_img.clear()

            pixmap2 = QPixmap()
            pixmap2.loadFromData(self.resize_video_img)

            # Включаем масштабирование содержимого
            self.ui.video_img.setScaledContents(False)

            # self.ui.lab_camera_img.setPixmap(QtGui.QPixmap(pixmap))
            self.ui.video_img.setPixmap(QtGui.QPixmap(pixmap2))

    def __show_hide_gate_control(self):
        if self.ui.gate_img.isHidden():
            self.ui.gate_img.show()
            self.ui.gate_open.show()
            self.show_gate_state = True
        else:
            self.ui.gate_open.hide()
            self.show_gate_state = False
            self.ui.gate_img.hide()

    # Раздел обновления кнопок ------------------------------------------------------------------
    def __while_update_buttons(self):
        """ Функция обновления списка кнопок по триггеру (Запускается в отдельном потоке)"""

        it_done = False

        while True:
            try:
                self.camera_list = CamerasRTPS.get_list(self.host, self.port, 'admin', 'admin')

                if len(self.camera_list) > 0:
                    self.camera_list.sort(key=lambda x: x['FName'])
                    self.signal_update_buttons.emit()
                # self.__create_buttons()
                # print(self.camera_list)
                break
            except Exception as ex:
                print(f"Exception in __while_update_buttons: {ex}")

            time.sleep(5)

    def __create_buttons(self):
        """ Пересоздает все кнопки связанные с выбором камеры """

        # Создаем контейнер-виджет
        if self.container_widget:
            self.container_widget.deleteLater()

        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)

        if self.list_widgets:
            for widget in self.list_widgets:
                widget.setParent(None)
                widget.destroy()
                # self.ui.verticalLayout_4.removeWidget(widget)

            self.list_widgets = list()

        # Удаляем растягивающее пространство
        item = self.ui.verticalLayout_2.takeAt(self.stretch_index)
        if item is not None:
            item.widget().deleteLater() if item.widget() else item.spacerItem().deleteLater()

        for data in self.camera_list:
            cam_name = data.get('FName')
            self.__add_label(cam_name)

        self.ui.verticalLayout_2.addStretch()

    def __add_label(self, cam_name: str):
        print(f"FName: {cam_name}")
        label_cam = QtWidgets.QLabel()   # self.ui.scrollAreaWidgetContents_2)
        label_cam.setMinimumSize(QtCore.QSize(120, 80))
        label_cam.setMaximumSize(QtCore.QSize(180, 100))
        label_cam.setStyleSheet("color: rgb(50, 50, 50); border: 1px solid; border-color: rgb(0,0,0);")
        label_cam.setObjectName(f"{cam_name}")
        label_cam.setText(cam_name)
        label_cam.setAlignment(Qt.Qt.AlignCenter)
        label_cam.mousePressEvent = (lambda ch, b=label_cam: self.chosen_camera_button(b))

        self.ui.verticalLayout_2.addWidget(label_cam)

        self.list_widgets.append(label_cam)

    def chosen_camera_button(self, btn: QtWidgets.QLabel):
        """ Тупо меняет переменную в классе которая отвечает за номер камеры в запросе,
        получаем данные из имени кнопки """

        name = btn.objectName()
        # self.ui.lab_cam_name.setText(f"Просмотр камеры: {name}")
        self.ui.gate_img.hide()
        self.ui.gate_open.hide()
        self.chosen_camera = name[3:len(name)]

    def do_screenshot(self):
        ChangeImg.save_screenshot(self.last_video_img, self.chosen_camera)

    # СОХРАНИНЕ РАЗМЕРОВ ПРОГРАММЫ С ПОСЛЕДНЕГО ЗАПУСКА
    def closeEvent(self, event):
        # Сохраняем параметры окна перед закрытием
        self.save_window_state()
        super().closeEvent(event)

    def save_window_state(self):
        # Сохраняем размер, позицию и состояние окна
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def restore_window_state(self):
        # Восстанавливаем размер, позицию и состояние окна
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        self.restoreState(self.settings.value("windowState", QByteArray()))

    def resizeEvent(self, event):
        # Вызываем resizeEvent родительского класса для корректной работы
        super().resizeEvent(event)

        # Устанавливаем размер QLabel равным размеру окна
        self.ui.video_img.resize(self.ui.video_img.size())
