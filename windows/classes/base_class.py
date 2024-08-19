""" Базовый класс содержащий базовые методы и общие переменные """
import datetime
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget

from PyQt5 import QtWidgets
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QSettings

from gui.test_gui import Ui_MainWindow
from misc.logger import Logger
from misc.settings import SettingsIni


logger = Logger()


class BaseWindow(QtWidgets.QMainWindow):

    def __init__(self, settings: SettingsIni):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(settings.window_title)

        # Настройки связи
        self.rtsp_host = settings.rtsp_host
        self.rtsp_port = settings.rtsp_port
        self.gate_driver_host = settings.apacs_gate_driver_host
        self.gate_driver_port = settings.apacs_gate_driver_port

        # Восстанавливаем сохраненные параметры окна
        self.settings = QSettings("VIG_TECH", "GUI_GATE_CONTROL")
        self.restore_window_state()

        # SCREENSHOT
        self.its_screenshot = False

        # Уведомление в интерфейсе
        self.new_msg = False
        self.last_msg = 'Нет событий'

        # Управление выбором камеры
        self.its_start = True
        self.chosen_camera = '0'
        self.device_con_thr = None

        # Создание новых кнопок для камер
        self.camera_list = list()
        self.list_widgets = list()
        self.container_widget = QWidget()
        self.stretch_index = 0
        self.fid_camera = dict()

        # Тригер переменная для прозрачной кнопки
        self.trigger_play = True

        # Отвечает за смену изображения в разделе для камеры и для статуса проезда
        # Загружаем GIF с помощью QMovie
        self.movie = QMovie("./gui/no-signal-stand-by.gif")
        self.switch_movie = True
        # self.label.setMovie(self.movie)

        # Переменные связанные с выводом изображения
        self.last_gate_img = b''
        self.last_video_img = b''

        self.resize_video_img = b''
        self.new_video_img = True
        self.time_new_video_img = datetime.datetime.now()

        self.size_video_wight = 1
        self.size_video_height = 1

        # Зона показать\спрятать управление проездом
        self.show_gate_state = True

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
