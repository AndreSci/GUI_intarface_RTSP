import socket
import threading
import time


def bin_to_hex(binary_string: str = '00000000'):

    # Преобразуем двоичную строку в целое число
    decimal_value = int(binary_string, 2)

    # Преобразуем целое число в шестнадцатеричное представление без префикса
    hex_value = f"{decimal_value:02x}"

    return hex_value


class DeviceServer:
    def __init__(self):
        self.last_state = b'#00000100'

        tr = threading.Thread(target=self.change_state, daemon=True)
        tr.start()

    def change_state(self):
        while True:
            time.sleep(1)
            # никого 1000 0001
            self.last_state = f'#100001{bin_to_hex("10000001")}'.encode()
            time.sleep(3)
            # машина у въезда закрыто 1000 1001
            self.last_state = f'#100001{bin_to_hex("10001001")}'.encode()
            time.sleep(1)
            # машина у въезда полу-открыт 1000 1000
            self.last_state = f'#100001{bin_to_hex("10001001")}'.encode()
            time.sleep(3)
            # машина у въезда открыто 1000 1010
            self.last_state = f'#100001{bin_to_hex("10001010")}'.encode()
            time.sleep(3)
            # машина первая половина в центр открыто 1000 1110
            self.last_state = f'#100001{bin_to_hex("10001110")}'.encode()
            time.sleep(3)
            # машина в центр открыто 1001 1110
            self.last_state = f'#100001{bin_to_hex("10011110")}'.encode()
            time.sleep(3)
            # машина вторая половина в центре открыто 1001 0110
            self.last_state = f'#100001{bin_to_hex("10010110")}'.encode()
            time.sleep(3)
            # машина в конце открыто 1001 0010
            self.last_state = f'#100001{bin_to_hex("10010010")}'.encode()
            time.sleep(3)
            # машины не открыто 1000 0010
            self.last_state = f'#100001{bin_to_hex("10000010")}'.encode()
            time.sleep(3)
            # машины не полу-открыто 1000 0000
            self.last_state = f'#100001{bin_to_hex("10000010")}'.encode()

    def process_message(self, message):
        # Проверка, что сообщение начинается с '#01' и достаточно длинное
        if message.startswith(b'#01') and len(message) == 9:
            # Возвращаем правильный ответ
            return b'#010000'
        elif message.startswith(b'#00') and len(message) == 9:
            # Возвращаем правильный ответ
            return self.last_state
        else:
            # Если формат не тот, возвращаем ошибочный ответ или ничего
            return b''

    def start_server(self, host='127.0.0.1', port=182):
        # Создаем сокет
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Связываем сокет с хостом и портом
        server_socket.bind((host, port))

        # Начинаем прослушивание
        server_socket.listen(5)
        print(f"Сервер запущен на {host}:{port}")

        while True:
            # Принимаем соединение
            client_socket, addr = server_socket.accept()
            print(f"Подключение от {addr}")

            # Читаем сообщение от клиента
            message = client_socket.recv(1024)
            print(f"Получено сообщение: {message}")

            # Обрабатываем сообщение
            response = self.process_message(message)

            # Отправляем ответ клиенту
            client_socket.sendall(response)
            print(f"Отправлен ответ: {response}")

            # Закрываем соединение
            client_socket.close()


if __name__ == "__main__":
    test_server = DeviceServer()
    test_server.start_server()


