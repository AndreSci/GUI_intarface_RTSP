import datetime

import requests
import cv2
import numpy as np
import io
from PIL import Image
from multiprocessing import Process
from socket_server.client import ClientSocket

URL = '0.0.0.0:80'
CAM_NUMBER = ['2']

URL_06 = '0.0.0.0:80'
# CAM_NUMBER_06 = ['01', '03', '05', '07']
CAM_NUMBER_06 = ['2']
# CAM_NUMBER_06 = ['01', '2', '03', '4', '05', '6', '07']

INDEX_PROC = 2
#
# CAM1=rtsp://192.168.20.226/h264
# CAM2=rtsp://192.168.0.55
# CAM3=rtsp://192.168.0.88
# CAM4=rtsp://192.168.0.74/sub
# CAM5=rtsp://192.168.0.93
# CAM6=rtsp://192.168.10.169/h264
#
# ;1Пандус обзор(20.249)
# CAM11=rtsp://192.168.20.249/main
#
# ;3Пандус обзор (0.54)
# CAM12=rtsp://192.168.0.54
#
# ;4Пандус обзор(0.89)
# CAM13=rtsp://192.168.0.89
#
# ;6Пандус обзор(0.73)
# CAM14=rtsp://192.168.0.73/sub
#
# ;8Пандус обзор(0.94)
# CAM15=rtsp://192.168.0.94


class RTSPConnect:
    @staticmethod
    def show_video(cam_num: str, url: str, test_num: int = 0, i: int = 0):
        print(f"Запуск процесса для камеры: {cam_num}")

        list_speed = list()
        max_index = 10000
        index = 0
        except_index = 0
        norm_index = 0
        requests_error_index = 0
        window_name = f"Test: {i} - {cam_num} - {test_num}"

        while index < max_index:
            index += 1
            start_time = datetime.datetime.now()

            if requests_error_index == 5:
                break

            try:
                res_req = requests.get(f"http://{url}/action.do?version=4.9.4"
                                       f"&command=frame.video&video_in=CAM:{cam_num}", timeout=3)
                # print(f"Got frame {index}")
                image = Image.open(io.BytesIO(res_req.content))

                # Изменяем позицию цветов местами для корректного отображения картинки
                red, green, blue = image.split()
                image = Image.merge("RGB", (blue, green, red))

                open_cv_image = np.array(image)

                cv2.imshow(window_name, open_cv_image)
                cv2.waitKey(1)

                high, weight = image.size

                if high > 400 and weight > 400:
                    norm_index += 1
            except requests.RequestException as rq:
                print(f"Time_out: {cam_num} -> {rq}")
                requests_error_index += 1
            except Exception as ex:
                except_index += 1
                if except_index >= 10:
                    print(f"Из-за множества ошибок был завершен цикл работы: {cam_num} -> {ex}")
                    break

            delta_time = datetime.datetime.now() - start_time
            list_speed.append(delta_time.total_seconds())
        try:
            cv2.destroyWindow(window_name)
        except Exception as ex:
            print(f"При попытке закрыть окно open-cv возникла ошибка: {ex}")

        print(f"Результат теста {test_num} связи с RTSP{cam_num}: удачных кадров: {norm_index}, "
              f"неудачных кадров: {max_index - norm_index}\n"
              f"Средняя скорость получения кадра: {sum(list_speed)/len(list_speed)} сек.")

    @staticmethod
    def show_video_socket(cam_num: str, url: str, test_num: int = 0, i: int = 0):
        print(f"Запуск процесса для камеры: {cam_num}")

        list_speed = list()
        max_index = 10000
        index = 0
        except_index = 0
        norm_index = 0
        requests_error_index = 0
        window_name = f"Test: {i} - {cam_num}"

        while index < max_index:
            index += 1
            start_time = datetime.datetime.now()

            if requests_error_index == 5:
                break

            try:
                # res_req = ClientSocket.take_frame(cam_num)
                res_req = ClientSocket.take_frame(cam_num)
                # print(f"Got frame {index}")
                image = Image.open(io.BytesIO(res_req))

                # Изменяем позицию цветов местами для корректного отображения картинки
                red, green, blue = image.split()
                image = Image.merge("RGB", (blue, green, red))

                open_cv_image = np.array(image)

                cv2.imshow(window_name, open_cv_image)
                cv2.waitKey(1)

                high, weight = image.size

                if high > 400 and weight > 400:
                    norm_index += 1
            except requests.RequestException as rq:
                print(f"Time_out: {cam_num} -> {rq}")
                requests_error_index += 1
            except Exception as ex:
                except_index += 1
                if except_index >= 10:
                    print(f"Из-за множества ошибок был завершен цикл работы: {cam_num} -> {ex}")
                    break

            delta_time = datetime.datetime.now() - start_time
            list_speed.append(delta_time.total_seconds())
        try:
            cv2.destroyWindow(window_name)
        except Exception as ex:
            print(f"При попытке закрыть окно open-cv возникла ошибка: {ex}")

        print(f"Результат теста {test_num} связи с RTSP{cam_num}: удачных кадров: {norm_index}, "
              f"неудачных кадров: {max_index - norm_index}\n"
              f"Средняя скорость получения кадра: {sum(list_speed)/len(list_speed)} сек.")


def test_1():
    """ Тест подключения к разным камерам """
    l = dict()
    test_num = 1

    for it in CAM_NUMBER_06:
        l[it] = Process(target=RTSPConnect.show_video, args=(it, URL_06, test_num), daemon=True)
        l[it].start()

    for it in l:
        l[it].join()


def test_2():
    """ Тест подключения множества клиентов к одной камере """
    n = 10
    l = dict()
    test_num = 5

    for i in range(n):
        for it in CAM_NUMBER:
            l[f"{i}_{it}"] = Process(target=RTSPConnect.show_video, args=(it, URL, i, test_num), daemon=True)
            l[f"{i}_{it}"].start()

    for i in range(n):
        for it in l:
            l[f"{it}"].join()


def test_3():
    """ Тест подключения множества клиентов к одной камере """
    n = 5
    l = dict()
    test_num = 2

    for i in range(n):
        for it in CAM_NUMBER:
            l[f"{i}_{it}"] = Process(target=RTSPConnect.show_video_socket, args=(it, URL, i, test_num), daemon=True)
            l[f"{i}_{it}"].start()

    for i in range(n):
        for it in l:
            l[f"{it}"].join()


if __name__ == "__main__":
    # test_1()
    test_2()
    # test_3()
