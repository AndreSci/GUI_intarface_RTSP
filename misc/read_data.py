from enum import Enum, unique

""" А. Инструкция по чтению состояния контроллера """
""" Документация по преобразованию шестнадцатеричный в двоичный HEX/BIN"""


# Принятые данные от контроллера -> b'#00000101'
# где # является стартовым символом
# 1. где b'#->00<-000101' является CMD (командой) доступно 256 значений
# 2. где b'#00->00<-0101' является EHS (на данный момент резерв)
# 3. где b'#0000->01<-01' является DS (размер следующих данных)
# 4. где b'#000001->01<-' является HEX данными которые нужно преобразовать в BIN -> (FF -> 11111111) \ (01 -> 0000 0001)
# HEX данные и их представление
# Инструкция по чтению преобразованных данных из пункта 4.
# 0000 0001 (не забываем что индексация происходит в обратном порядке)
# [7] - концевик закрыто        1\да 0\нет
# [6] - концевик открыто        1\да 0\нет
# [5] - Фотоэлемент             1\нет 0\да
# [4] - Индукционная петля А    1\нет авто 0\есть авто
# [3] - Индукционная петля Б    1\нет авто 0\есть авто
# [2] - РЕЗЕРВ
# [1] - РЕЗЕРВ
# [0] - Датчик наличия питания


@unique
class TypeBarrierStatus(Enum):
    CLOSED = 1
    OPENED = 2
    STUCK = 3


@unique
class TypeControllerStatus(Enum):
    CLOSED_INPUT_1 = 7
    OPENED_INPUT_2 = 6
    IK_PORT = 5
    LOOP_A = 4
    LOOP_B = 3
    UNKNOWN_A = 2
    UNKNOWN_B = 1
    POWER_ON = 0


class ReadData:

    @staticmethod
    def read_for_one(json_req: dict, fid: int) -> TypeBarrierStatus:

        ret_value = TypeBarrierStatus.STUCK

        result_req = json_req.get('RESULT')
        desc_req = json_req.get('DESC')
        data_req = json_req.get('DATA')

        if result_req == "SUCCESS":
            try:
                packet = data_req[str(fid)].get("Packet")
                end_res = packet.get('END_RES')

                input_number = end_res[0].get('input_number')
                input_state = end_res[0].get('state')

                ret_value = TypeBarrierStatus(int(input_state))
            except Exception as ex:
                print(f"Исключение в попытке получить данные: {ex}")
        else:
            pass

        return ret_value


class ReadCode:
    @staticmethod
    def read(code: str) -> dict:
        """
        {'position_barrier': barrier_pos,
                     'ik_port': ik_port,
                     'loop_a': loop_a,
                     'loop_b': loop_b,
                     'unknown_a': unknown_a,
                     'unknown_b': unknown_b,
                     'power_on': power_on
                     }
                     """

        input_1 = int(code[TypeControllerStatus.CLOSED_INPUT_1.value])
        input_2 = int(code[TypeControllerStatus.OPENED_INPUT_2.value])
        ik_port = int(code[TypeControllerStatus.IK_PORT.value])
        loop_a = int(code[TypeControllerStatus.LOOP_A.value])
        loop_b = int(code[TypeControllerStatus.LOOP_B.value])
        unknown_a = int(code[TypeControllerStatus.UNKNOWN_A.value])
        unknown_b = int(code[TypeControllerStatus.UNKNOWN_B.value])
        power_on = int(code[TypeControllerStatus.POWER_ON.value])

        barrier_pos = TypeBarrierStatus.STUCK

        if input_1 != input_2:
            if input_1 == 1:
                barrier_pos = TypeBarrierStatus.CLOSED
            else:
                barrier_pos = TypeBarrierStatus.OPENED

        ret_value = {'position_barrier': barrier_pos,
                     'ik_port': ik_port,
                     'loop_a': loop_a,
                     'loop_b': loop_b,
                     'unknown_a': unknown_a,
                     'unknown_b': unknown_b,
                     'power_on': power_on
                     }

        return ret_value


if __name__ == "__main__":
    print(TypeBarrierStatus(1))
