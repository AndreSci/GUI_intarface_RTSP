import os
import configparser
from misc.logger import Logger

logger = Logger()


class SettingsIni:

    def __init__(self):
        # general settings
        self.settings_file = configparser.ConfigParser()
        self.rtsp_host = ''
        self.rtsp_port = 0
        self.rtsp_socket_port = 0

    def load_data_from_file(self) -> dict:
        """ Функция получения настройки из файла settings.ini. """
        error_mess = 'Успешная загрузка данных из settings.ini'
        ret_value = dict()
        ret_value["result"] = False

        # проверяем файл settings.ini
        if os.path.isfile("./settings.ini"):
            try:
                self.settings_file.read("./settings.ini", encoding="utf-8")
                # general settings ----------------------------------------
                self.rtsp_host = self.settings_file["GENERAL"]["RTSP_HOST"]
                self.rtsp_port = self.settings_file["GENERAL"]["RTSP_PORT"]
                self.rtsp_socket_port = self.settings_file["GENERAL"].get("SOCKET_PORT")

                ret_value["result"] = True
            except KeyError as ex:
                error_mess = f"Не удалось найти поле в файле settings.ini: {ex}"
                logger.exception(error_mess)
                print(error_mess)
            except Exception as ex:
                error_mess = f"Не удалось прочитать файл: {ex}"
                print(error_mess)
        else:
            error_mess = "Файл settings.ini не найден в корне проекта"

        ret_value["desc"] = error_mess

        return ret_value


if __name__ == "__main__":
    ini = SettingsIni()
    print(ini.load_data_from_file())
