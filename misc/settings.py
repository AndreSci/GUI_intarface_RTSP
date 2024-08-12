import os
import configparser
from misc.logger import Logger

logger = Logger()


class SettingsIni:

    def __init__(self, file_address: str = "./settings.ini"):

        self.file_address = file_address
        self.settings_file = configparser.ConfigParser()

        self.window_title = 'Project'

        self.rtsp_host = '127.0.0.1'
        self.rtsp_port = 8093

        self.apacs_gate_driver_host = '127.0.0.1'
        self.apacs_gate_driver_port = 8080

        # Подгружаем данные из файла
        if not self.load_data_from_file():
            raise "Не удалось загрузить данные из файла"

    def load_data_from_file(self) -> bool:
        """ Функция получения настройки из файла settings.ini. """
        ret_value = False

        # проверяем файл settings.ini
        if os.path.isfile(self.file_address):
            try:
                self.settings_file.read(self.file_address, encoding="utf-8")
                # general settings ----------------------------------------
                self.window_title = self.settings_file['GEN']['TITLE']
                self.rtsp_host = self.settings_file["GEN"]["RTSP_HOST"]
                self.rtsp_port = self.settings_file["GEN"]["RTSP_PORT"]

                self.apacs_gate_driver_host = self.settings_file['GEN']['GATE_DRIVER_HOST']
                self.apacs_gate_driver_port = self.settings_file['GEN']['GATE_DRIVER_PORT']

                ret_value = True
            except KeyError as ex:
                error_mess = f"Не удалось найти поле в файле settings.ini: {ex}"
                logger.exception(error_mess)
            except Exception as ex:
                error_mess = f"Не удалось прочитать файл: {ex}"
                logger.exception(error_mess)

        return ret_value


if __name__ == "__main__":
    ini = SettingsIni()
    print(ini.load_data_from_file())
