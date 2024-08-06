

class ImgData:
    def __init__(self):
        self.images = {}

    def load(self):
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
