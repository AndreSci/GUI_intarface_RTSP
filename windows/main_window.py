import datetime
import threading
import time

import requests
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, QtNetwork
from PyQt5.Qt import QPushButton
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from gui.camera_gui import Ui_MainWindow
from enum import Enum
from misc.logger import Logger
from socket_server.client import ClientSocket, GifToBytes
from requests_to_rtsp.connection import CamerasRTPS
from misc.globals_value import GlobControlCamerasList, GlobalControl
from misc.read_data import TypeBarrierStatus, ReadData, ReadCode
from windows.button_cams import ButtonPic


logger = Logger()
NAME_VER = "VIG Camera Watcher + Gates Control"
TIME_CHECK_STATUS = 50  # ms.
BARRIER_FID = 2

# Тестовая заглушка
HOST = '192.168.15.10'
PORT = 8093


class ActionType(Enum):
    """ Служит для определения статуса действий """
    opened = 1
    closed = 2
    wait = 3


class Button(QPushButton):
    def __init__(self, num, text):  # !!!
        super().__init__()

        self.setText(f'{text}')  # !!! {text} {num}


class MainWindow(QtWidgets.QMainWindow):

    signal_status = QtCore.pyqtSignal(ActionType)
    signal_change_img = QtCore.pyqtSignal(bytes)
    signal_update_cams = QtCore.pyqtSignal()
    signal_update_button = QtCore.pyqtSignal(bytes, QtWidgets.QLabel, bool)
    signal_change_warning_msg = QtCore.pyqtSignal(str)

    def __init__(self, fid: int = None, host: str = None, port: int = None):
        super().__init__()

        self.update_buttons_img = False

        # QWidget
        self.list_widgets = list()

        self.camera_number = '0'

        self.time_last_update = datetime.datetime.now()

        # GlobControlCamerasList.update(CamerasRTPS.get_list(HOST, PORT, 'admin', 'admin'))

        if port:
            self.host = host
            self.port = port
            self.fid = fid
        else:
            self.host = HOST
            self.port = PORT
            self.fid = BARRIER_FID

        self.no_signal_class = GifToBytes()

        # self.tr = QThread()
        # self.tr.run = self.check_cams_status
        # self.tr.start()
        #
        # self.tr2 = QThread()
        # self.tr2.run = self.__while_update_cams
        # self.tr2.start()

        self.tr1 = threading.Thread(target=self.check_cams_status, daemon=True)
        self.tr1.start()
        self.tr2 = threading.Thread(target=self.__while_update_cams, daemon=True)
        self.tr2.start()

        # self.tr = QThread()
        # self.tr.run = self.check_gate_status
        # self.tr.start()

        # Блокируем запросы на обновление статуса и повторные отправки запросов
        self.action_not_lock = True

        # Объявляем интерфейс
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(NAME_VER)

        self.ui.Frame_Gate_Control.hide()

        # self.__create_buttons()
        # устанавливаем картинку шлагбаума
        self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/no_connection.jpg"))

        # buttons
        self.ui.but_update_cams.clicked.connect(self.__update_buttons_for_cams)
        self.ui.lab_camera_img.mousePressEvent = (lambda ch, b=12: self.__open_gate_control())

        # status
        self.action_type = ActionType.wait

        # signals
        self.signal_change_img.connect(self.__change_main_img)
        self.signal_update_cams.connect(self.__update_buttons_for_cams)
        self.signal_update_button.connect(self.__update_button_img)
        self.signal_change_warning_msg.connect(self.__update_warning_msg)

    def __update_warning_msg(self, text: str = None):
        """ Функция вывода сообщений в нижней части интерфейса """
        self.ui.warning_msg.setText(text)

    def __update_buttons_for_cams(self):
        """ Обновляем список камер и пересоздает все кнопки связанные с выбором камеры """
        data_now = datetime.datetime.now()

        if (data_now - self.time_last_update).total_seconds() > 1:
            self.time_last_update = datetime.datetime.now()
            GlobControlCamerasList.update(CamerasRTPS.get_list(HOST, PORT, 'admin', 'admin'))

            self.__create_buttons()

    def on_clicked(self, btn: QtWidgets.QLabel):
        """ Тупо меняет переменную в классе которая отвечает за номер камеры в запросе,
        получаем данные из имени кнопки """

        name = btn.objectName()
        self.ui.lab_cam_name.setText(f"Просмотр камеры: {name}")
        self.ui.Frame_Gate_Control.hide()
        self.camera_number = name[3:len(name)]

    def check_cams_status(self):
        """ Основной цикл смены изображения для выбранной камеры """
        no_signal_index = 0
        max_ns_index = GifToBytes.get_size() - 1

        while True:
            QThread.msleep(TIME_CHECK_STATUS)

            ret_value = ClientSocket.take_frame(self.camera_number)

            self.update_buttons_img = GlobalControl.test_speed(ret_value.size,
                                                               ret_value.time_start,
                                                               ret_value.time_end)

            if not self.update_buttons_img:
                text = f"Низкое качество связи, некоторые элементы интерфейса недоступны."
                print(text)
                self.signal_change_warning_msg.emit(text)

            if ret_value.result:
                self.signal_change_img.emit(ret_value.byte_img)
            else:
                if no_signal_index == max_ns_index:
                    no_signal_index = 0
                else:
                    no_signal_index += 1

                self.signal_change_img.emit(GifToBytes.get_img(no_signal_index))

    def __change_main_img(self, byte_img: bytes) -> None:
        """ Вызывается через сигнал и меняет изображение в главном секторе для отображения камеры """
        pixmap = QPixmap()

        # Put bytes of example.bmp into it
        pixmap.loadFromData(byte_img)
        pixmap = pixmap.scaled(self.ui.lab_camera_img.width(), self.ui.lab_camera_img.height())
        # TODO проверить производительность
        self.ui.lab_camera_img.setPixmap(QtGui.QPixmap(pixmap))

    def __while_update_cams(self):
        """ Функция служит для периодического обновления кнопок камер """

        self.signal_update_cams.emit()
        but_changer = None

        while True:
            # QThread.msleep(5000)
            time.sleep(5)

            if not but_changer:
                but_changer = ButtonPic(self.signal_update_button, self.list_widgets, self.update_buttons_img)
            elif but_changer.check_end():
                but_changer = ButtonPic(self.signal_update_button, self.list_widgets, self.update_buttons_img)

    def __create_buttons(self):
        """ Пересоздает все кнопки связанные с выбором камеры """
        step = 0

        if self.list_widgets:
            for widget in self.list_widgets:
                widget.setParent(None)
                widget.destroy()
                # self.ui.verticalLayout_4.removeWidget(widget)

            self.list_widgets = list()

        for cam_name in GlobControlCamerasList.get_list():
            step += 1
            self.__add_label(cam_name, step)

    def __open_gate_control(self):
        if self.ui.Frame_Gate_Control.isHidden():
            self.ui.Frame_Gate_Control.show()
        else:
            self.ui.Frame_Gate_Control.hide()

    def __add_label(self, cam_name: str, index: int):
        label_cam = QtWidgets.QLabel()   # self.ui.scrollAreaWidgetContents_2)
        label_cam.setMinimumSize(QtCore.QSize(120, 68))
        label_cam.setMaximumSize(QtCore.QSize(120, 100))
        label_cam.setStyleSheet("color: rgb(50, 50, 50); border: 1px solid; border-color: rgb(0,0,0);")
        label_cam.setObjectName(f"{cam_name}")
        label_cam.setText(cam_name)
        label_cam.setAlignment(Qt.Qt.AlignCenter)
        label_cam.mousePressEvent = (lambda ch, b=label_cam: self.on_clicked(b))

        self.ui.verticalLayout_4.addWidget(label_cam)

        self.list_widgets.append(label_cam)

    def __update_button_img(self, byte_img: bytes, btn: QtWidgets.QLabel, update_img: bool = False):

        if update_img:
            pixmap = QPixmap()
            pixmap.loadFromData(byte_img)
            size_but = btn.size()
            pixmap = pixmap.scaled(size_but.width(), size_but.height())

            btn.setPixmap(pixmap)
        else:
            btn.setText(btn.objectName())

    def check_gate_status(self):
        while True:
            QThread.msleep(1000)
            if self.action_not_lock:
                self.action_not_lock = False
                try:

                    # url = QtCore.QUrl("http://www.google.com")
                    #
                    # request = QNetworkRequest()
                    # request.setUrl(url)
                    # manager = QNetworkAccessManager()
                    #
                    # replyObject = manager.get(request)
                    # replyObject.finished.connect(self.handleResponse)

                    res = requests.get(f"http://{self.host}:{self.port}/GetBarrierState",
                                       params={'fid': self.fid})

                    json_req = res.json()
                    print(json_req)

                    if res.status_code == 200:
                        if json_req.get('RESULT') == 'SUCCESS':
                            # type_state = ReadData.read_for_one(json_req, self.fid)
                            type_state = ReadCode.read(json_req['DATA'][str(self.fid)]['Packet']['CONV'])
                            position_barrier = type_state.get('position_barrier')
                            loop_a = type_state.get('loop_a')
                            loop_b = type_state.get('loop_b')

                            if position_barrier == TypeBarrierStatus.CLOSED:
                                self.ui.text_status.setText("Закрыто")
                                self.action_type = ActionType.closed
                                self.ui.bt_open_close.setText("Открыть")
                                if loop_a == 1 or loop_b == 1:
                                    self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/closed_with_car.jpg"))
                                else:
                                    self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/closed.jpg"))

                            elif position_barrier == TypeBarrierStatus.OPENED:
                                self.ui.text_status.setText("Открыто")
                                self.action_type = ActionType.opened
                                self.ui.bt_open_close.setText("Закрыть")
                                if loop_a == 1 or loop_b == 1:
                                    self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/opened_with_car.jpg"))
                                else:
                                    self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/opened.jpg"))
                            else:
                                self.ui.text_status.setText("Нет связи")
                                self.ui.bt_open_close.setText("Октрыть")
                                self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/no_connection.jpg"))

                        elif json_req.get('RESULT') == 'ERROR':
                            self.ui.text_status.setText("Не удалось получить статус")
                            self.action_type = ActionType.wait
                    else:
                        self.ui.text_status.setText("Сервис временно недоступен")
                        self.action_type = ActionType.wait

                except Exception as ex:
                    logger.exception(f"Exception in: {ex}")
                    self.ui.text_status.setText("Сервис временно недоступен")
                    self.action_type = ActionType.wait
                finally:
                    self.action_not_lock = True

            QThread.msleep(TIME_CHECK_STATUS)

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))

        else:
            print("Error occured: ", er)
            print(reply.errorString())