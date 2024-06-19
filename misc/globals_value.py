RTSP_URL = '192.168.15.10'
RTSP_PORT = 8093

LIST_CAMERAS = ['CAM1', 'CAM2', 'CAM3', 'CAM4', 'CAM5', 'CAM6', 'CAM07']


class GlobControlCamerasList:
    @staticmethod
    def update(values: dict) -> list:
        global LIST_CAMERAS
        ret_value = list()

        ret_value.append('NoConnection')

        for it in values:
            ret_value.append(str(it.get('FName')))

        if len(ret_value) > 1:
            LIST_CAMERAS = ret_value

        return ret_value

    @staticmethod
    def get_list() -> list:
        return LIST_CAMERAS


class GlobalControl:
    @staticmethod
    def change_rtsp(url: str, port: int):
        global RTSP_URL, RTSP_PORT

        RTSP_URL = str(url)
        RTSP_PORT = int(port)

    @staticmethod
    def get_rtsp():
        return RTSP_URL, RTSP_PORT
