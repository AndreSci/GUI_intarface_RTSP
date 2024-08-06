from enum import Enum, unique
from datetime import datetime,timedelta
from windows.image_loader import ImgData

TIME_BETWEEN_CAR = 2  # sec.


@unique
class ObjectPosition(Enum):
    NONE = 0
    EXIT = 5
    ENTRY = 6


class GuiImage(ImgData):
    """ Класс загрузки и выдачи картинок связанных с отображением шлагбаума """
    def __init__(self):
        super().__init__()
        pass

    def get_car_entry(self, gate_position: int, object_in: int) -> bytes:
        return self.images.get(f'entry{gate_position}{object_in}')

    def get_no_car(self, gate_position: int) -> bytes:
        return self.images.get(f'none{gate_position}')

    def get_car_exit(self, gate_position: int, object_in: int) -> bytes:
        return self.images.get(f'exit{gate_position}{object_in}')


class ControlUseImg(GuiImage):
    """ Класс распределения запроса на получения картинки """
    def __init__(self):
        super().__init__()
        self.spend_from_pos = datetime.now() - timedelta(seconds=5)  # Для исключения ошибка при запуске
        self.last_position = ObjectPosition.NONE

    def __get_with_pos(self, position: int, gate_position: int, object_in: int = 0) -> bytes:
        ret_value = b''

        if position == ObjectPosition.ENTRY.value:
            # ENTRY
            ret_value = self.get_car_entry(gate_position, object_in)
        elif position == ObjectPosition.EXIT.value:
            # EXIT
            ret_value = self.get_car_exit(gate_position, object_in)
        else:
            # ДУМАЕМ
            ret_value = self.get_no_car(gate_position)

        return ret_value

    def get_img(self, gate_position: int, object_in: int = 0) -> bytes:

        ret_value = b''

        if gate_position and object_in != 0:
            time_passes = int(datetime.now() - self.spend_from_pos)

            if time_passes < TIME_BETWEEN_CAR:
                # Если время делаем начальную позицию last_position
                self.spend_from_pos = datetime.now()
                ret_value = self.__get_with_pos(self.last_position.value, gate_position, object_in)
            elif object_in == ObjectPosition.ENTRY.value:
                self.last_position = ObjectPosition.ENTRY
                self.spend_from_pos = datetime.now()
                ret_value = self.__get_with_pos(self.last_position.value, gate_position, object_in)
            elif object_in == ObjectPosition.EXIT.value:
                self.last_position = ObjectPosition.EXIT
                self.spend_from_pos = datetime.now()
                ret_value = self.__get_with_pos(self.last_position.value, gate_position, object_in)
            else:
                # Если прошло больше времени считаем что начался новый цикл нахождения машины
                ret_value = self.__get_with_pos(object_in, gate_position, object_in)

        else:
            ret_value = self.get_no_car(gate_position)

        return ret_value
