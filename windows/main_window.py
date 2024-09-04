import datetime
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from requests_to_rtsp.connection import CamerasRTPS
from gate_driver.connection import GateDriver, GateStateClass
from misc.brightness_factor import increase_brightness
from windows.button_cams import ButtonPic

from misc.resize_img import ChangeImg
from misc.logger import Logger
from misc.settings import SettingsIni
from windows.image_control import ControlUseImg
from windows.image_loader import SwitchCameraImg

from windows.classes.base_class import BaseWindow


logger = Logger()


class ThreadImgControl(QThread):
    """ Класс поток отвечает за обновление кадров в окне """
    change_img = pyqtSignal()

    def run(self):
        while True:
            QThread.msleep(200)
            self.change_img.emit()


class ThreadMsgControl(QThread):
    """ Класс поток отвечает за обновление сообщений в окне """
    update_msg = pyqtSignal()

    def run(self):
        while True:
            QThread.msleep(100)
            self.update_msg.emit()


class MainWindow(BaseWindow):
    signal_update_buttons = QtCore.pyqtSignal()
    signal_update_msg_label = QtCore.pyqtSignal()
    signal_update_img_buttons = QtCore.pyqtSignal()
    signal_update_button = QtCore.pyqtSignal(bytes, QtWidgets.QLabel, bool)

    def __init__(self, settings: SettingsIni):
        super().__init__(settings)

        # Настраиваем положение окон отображения изображения
        # Комментарий: супер не очевидно, но это работает ....
        self.ui.horizontalLayout_5.setStretch(0, 3)
        self.ui.horizontalLayout_5.setStretch(1, 1)

        # self.ui.verticalLayout_2.addStretch()

        # DEVICE CONNECTION
        self.device_connection = GateDriver(self.gate_driver_host, self.gate_driver_port)
        self.gate_state = GateStateClass()

        # Создаем прозрачную кнопку
        self.__create_player_frame()
        self.__create_play_button()

        # Создаем фоновые действия
        self.img_cont = ControlUseImg()

        # Отвечает за структурное переключение между камерами
        self.switch_camera_img = SwitchCameraImg()
        self.trigger_switch_cam = False

        self.qtr1 = ThreadImgControl()
        self.qtr1.change_img.connect(self.__while_img)
        self.qtr1.start()

        self.qtr_msg = ThreadMsgControl()
        self.qtr_msg.update_msg.connect(self.__while_msg)
        self.qtr_msg.start()
        # tr1 = threading.Thread(target=self.__while_img, daemon=True)
        # tr1.start()

        self.tr_device = threading.Thread(target=self.__while_device_state, daemon=True)
        self.tr_device.start()

        self.tr_buts_img = threading.Thread(target=self.__while_update_img_buttons, daemon=True)
        self.tr_buts_img.start()

        self.tr_buttons = threading.Thread(target=self.__while_update_buttons, daemon=True)
        self.tr_buttons.start()

        self.tr_video = threading.Thread(target=self.__rtsp_http_get, daemon=True)
        self.tr_video.start()

        self.ui.video_img.mousePressEvent = (lambda ch, b='0': self.__show_hide_gate_control())

        self.signal_update_buttons.connect(self.__create_buttons)
        self.signal_update_button.connect(self.__update_button_img)

        # Кнопки
        self.ui.screen_shot.clicked.connect(self.do_screenshot)
        self.ui.gate_open.clicked.connect(self.__pulse_device)

    # Визуал кнопки ---------------------------------------
    def __create_play_button(self):
        # Создаем прозрачную кнопку
        self.play_button = QtWidgets.QPushButton('СТОП', self.ui.video_img)
        self.from_left = 100
        self.from_bottom = 40
        self.button_height = 50
        self.button_width = 50

        self.play_button.clicked.connect(self.__play_button_switch)

        self.__update_position_play_button()

    def __play_button_switch(self, turn_on: bool = False):
        if turn_on:
            self.trigger_play = False

        if self.trigger_play:
            self.play_button.setText('СТАРТ')
            self.trigger_play = False
            self.new_event_msg("Видео остановлено.")
        else:
            self.play_button.setText('СТОП')
            self.trigger_play = True
            self.new_event_msg("Видео включено.")

    def __update_position_play_button(self):
        # Устанавливаем прозрачный фон кнопки
        self.play_button.setStyleSheet("QPushButton { color:rgb(255,255,255); background-color: rgba(255,255,255,0); "
                                          "border: 2px solid; border-radius: 25px; border-color: rgb(255,255,255);} "
                                          "QPushButton:hover { background-color: rgba(245, 245, 245, 25); } "
                                          "QPushButton:pressed { background-color: rgba(235, 235, 235, 50);}")

        self.label_height = self.ui.video_img.height()

        self.play_button.setGeometry(self.from_left, self.label_height - self.button_height - self.from_bottom,
                                     self.button_width,
                                     self.button_height)

    def __create_player_frame(self):
        # Создаем прозрачную кнопку
        self.player_frame = QtWidgets.QFrame(self.ui.video_img)
        self.player_frame_from_left = 0
        self.player_frame_height = 125
        self.player_frame_width = 500

        self.__update_player_frame()

    def __update_player_frame(self):
        # Устанавливаем прозрачный фон кнопки
        self.player_frame.setStyleSheet("background-color: rgba(255,255,255,25); border: 0px solid;")

        self.label_height = self.ui.video_img.height()
        self.label_player_width = self.ui.video_img.width()

        self.player_frame.setGeometry(self.player_frame_from_left, self.label_height - self.player_frame_height,
                                         self.label_player_width,
                                         self.player_frame_height)

    # MSG WATCHER ------------------------------------------
    def __while_msg(self):
        if self.new_msg:
            self.new_msg = False
            self.ui.msg_event.setText(self.last_msg)
            self.ui.msg_name_camera.setText(self.chosen_camera)

    def new_event_msg(self, text: str):
        self.last_msg = text
        self.new_msg = True

    # BUTTONS ----------------------------------------------
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

    def __while_update_img_buttons(self):
        """ Функция служит для периодического обновления кнопок камер """

        self.signal_update_img_buttons.emit()
        but_changer = None

        while True:
            # QThread.msleep(5000)
            time.sleep(5)

            if not but_changer:
                but_changer = ButtonPic(self.signal_update_button, self.list_widgets,
                                        self.rtsp_host,
                                        self.rtsp_port)
            elif but_changer.check_end():
                but_changer = ButtonPic(self.signal_update_button, self.list_widgets,
                                        self.rtsp_host,
                                        self.rtsp_port)

    # DEVICE ACTION ----------------------------------------
    def __while_device_state(self):
        while True:
            time.sleep(0.1)
            self.__get_state()

    def __pulse_device(self):
        for camera in self.camera_list:
            # Написано в спешке вечером в пятницу....
            if camera['FName'] == f"CAM{self.chosen_camera}":
                self.new_event_msg('Отправлен запрос на открытие проезда.')
                self.device_con_thr = threading.Thread(target=self.device_connection.pulse_device,
                                                       args=[camera['FID'],], daemon=True)
                self.device_con_thr.start()
                break

    def __get_state(self):
        cam_fid = -1
        if f"CAM{self.chosen_camera}" in self.fid_camera:
            cam_fid = self.fid_camera[f"CAM{self.chosen_camera}"]

        if cam_fid == -1:
            for camera in self.camera_list:
                # Написано в спешке вечером в пятницу....
                if camera['FName'] == f"CAM{self.chosen_camera}":
                    self.fid_camera[f"CAM{self.chosen_camera}"] = camera['FID']
                    break

        if cam_fid >= 0:
            self.gate_state = self.device_connection.get_state(cam_fid)
        else:
            self.new_event_msg('Не удалось найти управление проездом для данной камеры')

    # RTSP ACTION -------------------------------------------
    def __rtsp_http_get(self):
        """ Отвечает за получение кадров из RTSP сервера по имени камеры"""

        while True:
            frame_res = CamerasRTPS.get_frame(self.rtsp_host, self.rtsp_port, self.chosen_camera)

            # 'trigger_switch_cam = True' убирает случай когда был получен запрос на смену камеры,
            # но в этот момент уже был отправлен запрос на получения нового кадра,
            # что приводило к выводу картинки из предыдущей камеры.
            if frame_res.result and not self.trigger_switch_cam:
                self.new_video_img = True
                self.time_new_video_img = datetime.datetime.now()
                self.last_video_img = frame_res.byte_img
            else:
                self.trigger_switch_cam = False

    def __while_img(self):
        if self.trigger_play:
            self.__change_main_img(self.img_cont.get_img(self.gate_state.gate_position, self.gate_state.object_in))

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
                print("ВКЛЮЧАЮ ВИДЕО <------------------------------------------------")
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

            if self.its_screenshot:
                self.its_screenshot = False
                try:
                    self.resize_video_img = increase_brightness(self.resize_video_img, 2)
                except Exception as ex:
                    print(f"{ex}")

            pixmap2 = QPixmap()
            pixmap2.loadFromData(self.resize_video_img)

            # Выключаем масштабирование содержимого
            self.ui.video_img.setScaledContents(False)

            # Выравнивание изображения по центру
            self.ui.video_img.setAlignment(Qt.Qt.AlignCenter)

            # Перемещаем кнопку при изменении размера окна
            self.__update_position_play_button()
            self.__update_player_frame()

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

    # Раздел обновления кнопок ------------------------------
    def __while_update_buttons(self):
        """ Функция обновления списка кнопок по триггеру (Запускается в отдельном потоке)"""

        while True:
            try:
                self.camera_list = CamerasRTPS.get_list(self.rtsp_host, self.rtsp_port, 'admin', 'admin')
                print(self.camera_list)

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

        if self.its_start:
            # Заглушка чтоб при открытии программы сразу показывала первую камеру
            self.its_start = False
            self.chosen_camera = cam_name[3:]
            self.ui.msg_name_camera.setText(cam_name[3:])

        label_cam = QtWidgets.QLabel()   # self.ui.scrollAreaWidgetContents_2)
        label_cam.setMinimumSize(QtCore.QSize(170, 100))
        label_cam.setMaximumSize(QtCore.QSize(170, 100))
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

        self.last_video_img = self.switch_camera_img.get_switch_cam()
        self.time_new_video_img = datetime.datetime.now()
        self.new_video_img = True
        self.trigger_switch_cam = True

        name = btn.objectName()
        # self.ui.lab_cam_name.setText(f"Просмотр камеры: {name}")
        self.ui.gate_img.hide()
        self.ui.gate_open.hide()
        self.chosen_camera = name[3:len(name)]
        self.new_msg = True

        self.__play_button_switch(turn_on=True)

    # СКРИНШОТ ----------------------------------------------
    def do_screenshot(self):
        self.its_screenshot = True
        try:
            ChangeImg.save_screenshot(self.last_video_img, self.chosen_camera)
            self.new_event_msg('Сделан новый снимок экрана.')
        except Exception as ex:
            print(f"Exception in: {ex}")
            self.new_event_msg(f"не удалось сделать снимок.")

    def resizeEvent(self, event):
        # Вызываем resizeEvent родительского класса для корректной работы
        super().resizeEvent(event)

        # Устанавливаем размер QLabel равным размеру окна
        self.ui.video_img.resize(self.ui.video_img.size())

        # Перемещаем кнопку при изменении размера окна
        self.__update_position_play_button()
        self.__update_player_frame()
