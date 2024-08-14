import requests

from misc.speed_test_decor import ShowWorkSpeed


class GateStateClass:
    def __init__(self):
        self.gate_position = 7
        self.object_in = 0
        self.power = 0
        self.reserve_a = 0
        self.reserve_b = 0


class GateDriver:
    """ На этапе разработки драйвер управления контроллерами расположен в интерфейсе Apacs3000 """
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

    def get_state(self, camera_id: int) -> GateStateClass:
        ret_value = GateStateClass()

        try:
            req_str = f"http://{self.host}:{self.port}/StateByCameraID?fid={camera_id}"

            res_req = requests.get(req_str, timeout=3)

            json_req = res_req.json()

            if json_req and json_req.get('RESULT') == "SUCCESS":
                device_data = json_req['DATA']
                ret_value.gate_position = device_data['decode_data'][0].get('gate_position')
                ret_value.object_in = device_data['decode_data'][0].get('object_in')
                ret_value.power = device_data['decode_data'][0].get('power')
                ret_value.reserve_a = device_data['decode_data'][0].get('reserve_a')
                ret_value.reserve_b = device_data['decode_data'][0].get('reserve_b')

        except Exception as ex:
            print(f"Exception in GateDriver.get_state: {ex}")

        return ret_value
