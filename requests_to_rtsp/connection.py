import requests
import datetime
from misc.globals_value import HOST_RTSP, PORT_RTSP


class PairRetValue:

    def __init__(self):
        self.result = False
        self.byte_img = b''
        self.size = 0
        self.time_start = datetime.datetime.now()
        self.time_end = datetime.datetime.now()


class CamerasRTPS:
    @staticmethod
    def get_list(url: str, port: str, user: str, password: str) -> dict:

        ret_value = dict()

        try:
            res_request = requests.get(f"http://{url}:{port}/action.get_cameras?user={user}&password={password}",
                                       timeout=3)
            json_req = res_request.json()

            if json_req.get('RESULT') == 'SUCCESS':
                ret_value = json_req.get('DATA')
            else:
                print(json_req)

        except Exception as ex:
            print(f"Exception in: {ex}")

        return ret_value

    @staticmethod
    def get_frame(cam_num: str) -> PairRetValue:
        ret_value = PairRetValue()

        try:
            res_req = requests.get(f"http://{HOST_RTSP}:{PORT_RTSP}/action.do?video_in=CAM:{cam_num}", timeout=3)

            if res_req.status_code == 200:
                ret_value.result = True
                ret_value.byte_img = res_req.content
                ret_value.size = len(ret_value.byte_img)
            else:
                print(res_req.status_code)

        except Exception as ex:
            print(f"Exception in: {ex}")

        return ret_value
