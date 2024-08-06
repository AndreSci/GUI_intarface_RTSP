import datetime
import threading
import time
import requests

from windows.class_main import MainClass, ActionType

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


logger = Logger()


class Button(QPushButton):
    def __init__(self, num, text):  # !!!
        super().__init__()

        self.setText(f'{text}')  # !!! {text} {num}


class MainWindow(MainClass):

    def __init__(self, host: str = None, port: int = None):
        super().__init__(host, port)

        self.update_buttons_img = False

        self.opened_gate_windows = False

        self.time_last_update = datetime.datetime.now()

        # GlobControlCamerasList.update(CamerasRTPS.get_list(host, port, 'admin', 'admin'))

        self.fid = BARRIER_FID

        self.no_signal_class = GifToBytes()

        self.tr1 = threading.Thread(target=self.check_cams_status, daemon=True)
        self.tr1.start()
        self.tr2 = threading.Thread(target=self.__while_update_cams, daemon=True)
        self.tr2.start()

        # self.tr = QThread()
        # self.tr.run = self.check_gate_status
        # self.tr.start()

        # Блокируем запросы на обновление статуса и повторные отправки запросов
        self.action_not_lock = True

        self.ui.Frame_Gate_For_Hide.hide()

        # self.__create_buttons()
        # устанавливаем картинку шлагбаума
        self.ui.gate_state_img.setPixmap(QtGui.QPixmap("./gui/no_connection.jpg"))

        # buttons
        self.ui.lab_camera_img.mousePressEvent = (lambda ch, b=12: self.__open_gate_control())

        # status
        self.action_type = ActionType.wait

        # signals
        self.signal_change_img.connect(self.__change_main_img)
        self.signal_change_warning_msg.connect(self.__update_warning_msg)

    def __update_warning_msg(self, text: str = None):
        """ Функция вывода сообщений в нижней части интерфейса """
        self.ui.warning_msg.setText(text)

    def check_cams_status(self):
        """ Основной цикл смены изображения для выбранной камеры """
        no_signal_index = 0
        max_ns_index = GifToBytes.get_size() - 1

        while True:
            QThread.msleep(TIME_CHECK_STATUS)

            # ret_value = ClientSocket.take_frame(self.camera_number)
            ret_value = CamerasRTPS.get_frame(self.host, self.port, self.camera_number)

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

        if self.window_number == 3:
            window_width = self.ui.cam_img_3.width()
            window_height = self.ui.cam_img_3.height()
        else:
            window_width = self.ui.lab_camera_img.width()
            window_height = self.ui.lab_camera_img.height()

        byte_img = ChangeImg.resize(byte_img, window_width, window_height)

        pixmap = QPixmap()
        pixmap.loadFromData(byte_img)
        # self.ui.lab_camera_img.setPixmap(QtGui.QPixmap(pixmap))
        if self.window_number == 3:
            self.ui.cam_img_3.setPixmap(QtGui.QPixmap(pixmap))
        else:
            self.ui.cam_img_3.setPixmap(QtGui.QPixmap(pixmap))

    def __while_update_cams(self):
        """ Функция служит для периодического обновления кнопок камер """

        self.signal_update_cams.emit()
        but_changer = None

        while True:
            # QThread.msleep(5000)
            time.sleep(5)

            if not but_changer:
                but_changer = ButtonPic(self.signal_update_button, self.list_widgets,
                                        self.host,
                                        self.port,
                                        self.update_buttons_img)
            elif but_changer.check_end():
                but_changer = ButtonPic(self.signal_update_button, self.list_widgets,
                                        self.host,
                                        self.port,
                                        self.update_buttons_img)

    def __open_gate_control(self):
        if self.ui.Frame_Gate_For_Hide.isHidden():
            self.ui.Frame_Gate_For_Hide.show()
            self.opened_gate_windows = True
        else:
            self.opened_gate_windows = False
            self.ui.Frame_Gate_For_Hide.hide()

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
