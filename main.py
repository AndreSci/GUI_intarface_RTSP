from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from windows.main_window import MainWindow


def main():
    app_gui = QtWidgets.QApplication(sys.argv)
    app_gui.setWindowIcon(QtGui.QIcon('icon.png'))
    gui_app = MainWindow()

    gui_app.show()

    sys.exit(app_gui.exec())


if __name__ == "__main__":
    main()

# pyuic5 -x ./gui/untitled.ui -o ./gui/camera_gui.py
# 01. pip install pyinstaller
# 02. pip install pyinstaller==5.13.2  (cancel windows defender error)
# 03. auto-py-to-exe
