import requests
import datetime


class PairRetValue:

    def __init__(self):
        self.result = False
        self.byte_img = b''
        self.size = 0
        self.time_start = datetime.datetime.now()
        self.time_end = datetime.datetime.now()

    def __str__(self):
        return f"result: {self.result} size: {self.size} time_start: {self.time_start}"


class CamerasRTPS:
    @staticmethod
    def get_list(host: str, port: str, user: str, password: str) -> list:

        ret_value = list()

        try:
            req_str = f"http://{host}:{port}/action.get_cameras?user={user}&password={password}"

            res_request = requests.get(req_str, timeout=3)
            json_req = res_request.json()

            if json_req.get('RESULT') == 'SUCCESS':
                ret_value = json_req.get('DATA')
            else:
                print(json_req)

        except Exception as ex:
            print(f"Exception in: {ex}")

        return ret_value

    @staticmethod
    def get_frame(host: str, port: int, cam_num: str) -> PairRetValue:
        ret_value = PairRetValue()

        try:
            req_str = f"http://{host}:{port}/action.do?video_in=CAM:{cam_num}"

            res_req = requests.get(req_str, timeout=3)

            if res_req.status_code == 200:
                ret_value.result = True
                ret_value.byte_img = res_req.content
                ret_value.size = len(ret_value.byte_img)
            else:
                print(res_req.status_code)

        except Exception as ex:
            print(f"Exception in: {ex}")

        return ret_value
