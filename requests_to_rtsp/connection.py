import requests
from PyQt5.QtNetwork import QNetworkRequest


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
