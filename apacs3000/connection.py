import requests


class Apacs3000:
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):

        self.host = host
        self.port = port

    def pulse_device(self, camera_id: int) -> str:

        ret_value = str()

        try:
            req_str = f"http://{self.host}:{self.port}/PulseByCameraID?fid={camera_id}"

            res_req = requests.get(req_str, timeout=3)

            json_req = res_req.json()

            if json_req and json_req.get('RESULT') == "SUCCESS":
                ret_value = "Успешно выполнена команда"
            else:
                ret_value = "Не удалось выполнить команду"

        except Exception as ex:
            print(f"Exception in: {ex}")

        return ret_value
