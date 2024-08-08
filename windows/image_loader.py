from PIL import Image
import io


def load_image_as_bytes(file_path):
    with Image.open(file_path) as img:
        byte_arr = io.BytesIO()
        img.save(byte_arr, format=img.format)
        byte_code = byte_arr.getvalue()
    return byte_code


class ImgData:
    def __init__(self):
        self.images = {}

        self.load()

    def load(self):
        # Въезд
        self.images['entry96'] = load_image_as_bytes("./gui/gates/car_entry_close.jpg")
        self.images['entry106'] = load_image_as_bytes("./gui/gates/car_entry_average.jpg")
        self.images['entry86'] = load_image_as_bytes("./gui/gates/car_entry_open.jpg")
        self.images['entry81'] = load_image_as_bytes("./gui/gates/car_entry_open_center.jpg")
        self.images['entry82'] = load_image_as_bytes("./gui/gates/car_entry_open_mid_start.jpg")
        self.images['entry83'] = load_image_as_bytes("./gui/gates/car_entry_open_mid_end.jpg")
        self.images['entry85'] = load_image_as_bytes("./gui/gates/car_entry_open_end.jpg")

        # Выезд
        self.images['exit95'] = load_image_as_bytes("./gui/gates/car_exit_close.jpg")
        self.images['exit105'] = load_image_as_bytes("./gui/gates/car_exit_average.jpg")
        self.images['exit85'] = load_image_as_bytes("./gui/gates/car_exit_open.jpg")
        self.images['exit81'] = load_image_as_bytes("./gui/gates/car_exit_open_center.jpg")
        self.images['exit82'] = load_image_as_bytes("./gui/gates/car_exit_open_mid_end.jpg")
        self.images['exit83'] = load_image_as_bytes("./gui/gates/car_exit_open_mid_start.jpg")
        self.images['exit86'] = load_image_as_bytes("./gui/gates/car_exit_open_end.jpg")

        # Без машины
        self.images['none7'] = load_image_as_bytes("./gui/gates/no_signal.jpg")
        self.images['none8'] = load_image_as_bytes("./gui/gates/open.jpg")
        self.images['none9'] = load_image_as_bytes("./gui/gates/close.jpg")
        self.images['none10'] = load_image_as_bytes("./gui/gates/average.jpg")

        self.images['object84'] = load_image_as_bytes("./gui/gates/open_object_in_warning.jpg")
        self.images['object94'] = load_image_as_bytes("./gui/gates/close_object_in_warning.jpg")
        self.images['object104'] = load_image_as_bytes("./gui/gates/average_object_in_warning.jpg")

    def load_old(self):
        # Въезд
        with open("./gui/gates/car_entry_close.jpg") as file:
            bytes_img = file.read()
            self.images['entry96'] = bytes_img

        with open("./gui/gates/car_entry_average.jpg") as file:
            bytes_img = file.read()
            self.images['entry106'] = bytes_img

        with open("./gui/gates/car_entry_open.jpg") as file:
            bytes_img = file.read()
            self.images['entry86'] = bytes_img

        with open("./gui/gates/car_entry_open_center.jpg") as file:
            bytes_img = file.read()
            self.images['entry81'] = bytes_img

        with open("./gui/gates/car_entry_open_end.jpg") as file:
            bytes_img = file.read()
            self.images['entry83'] = bytes_img

        # Выезд

        with open("./gui/gates/car_exit_close.jpg") as file:
            bytes_img = file.read()
            self.images['exit95'] = bytes_img

        with open("./gui/gates/car_exit_average.jpg") as file:
            bytes_img = file.read()
            self.images['exit105'] = bytes_img

        with open("./gui/gates/car_exit_open.jpg") as file:
            bytes_img = file.read()
            self.images['exit85'] = bytes_img

        with open("./gui/gates/car_exit_open_center.jpg") as file:
            bytes_img = file.read()
            self.images['exit81'] = bytes_img

        with open("./gui/gates/car_exit_open_end.jpg") as file:
            bytes_img = file.read()
            self.images['exit83'] = bytes_img

        # Без машины

        with open("./gui/gates/no_signal.jpg") as file:
            bytes_img = file.read()
            self.images['none7'] = bytes_img

        with open("./gui/gates/open.jpg") as file:
            bytes_img = file.read()
            self.images['none8'] = bytes_img

        with open("./gui/gates/close.jpg") as file:
            bytes_img = file.read()
            self.images['none9'] = bytes_img

        with open("./gui/gates/average.jpg") as file:
            bytes_img = file.read()
            self.images['none10'] = bytes_img

