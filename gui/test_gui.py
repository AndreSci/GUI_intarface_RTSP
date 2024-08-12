# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/test_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1725, 883)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("border: 1px solid;\n"
"border-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(210, 230))
        self.frame_2.setMaximumSize(QtCore.QSize(420, 16777215))
        self.frame_2.setStyleSheet("border: 1px solid;\n"
"border-color: rgb(0, 0, 0);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.buttons_vbox = QtWidgets.QVBoxLayout()
        self.buttons_vbox.setObjectName("buttons_vbox")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 558))
        self.scrollArea.setStyleSheet("border: 0px, solid;")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 206, 841))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.buttons_vbox.addWidget(self.scrollArea)
        self.verticalLayout_3.addLayout(self.buttons_vbox)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setStyleSheet("border: 1px solid;\n"
"border-color: rgb(0, 0, 0);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gate_img = QtWidgets.QLabel(self.page)
        self.gate_img.setMinimumSize(QtCore.QSize(300, 0))
        self.gate_img.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid;\n"
"border-color: rgb(0, 0, 0);")
        self.gate_img.setText("")
        self.gate_img.setObjectName("gate_img")
        self.horizontalLayout_5.addWidget(self.gate_img)
        self.video_img = QtWidgets.QLabel(self.page)
        self.video_img.setMinimumSize(QtCore.QSize(500, 0))
        self.video_img.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border: 1px solid;\n"
"border-color: rgb(0, 0, 0);")
        self.video_img.setText("")
        self.video_img.setObjectName("video_img")
        self.horizontalLayout_5.addWidget(self.video_img)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.frame_4 = QtWidgets.QFrame(self.page)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_4.setStyleSheet("border: 0px solid;\n"
"border-color: rgb(0, 0, 0);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_7.setSpacing(1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 96))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.screen_shot = QtWidgets.QPushButton(self.frame_5)
        self.screen_shot.setGeometry(QtCore.QRect(30, 20, 131, 51))
        self.screen_shot.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 1px solid;\n"
"    border-radius: 6px;\n"
"    color: rgb(0,0, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(245, 245, 245);\n"
"    color: rgb(55, 55, 55);\n"
"\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(235, 235, 235);\n"
"}")
        self.screen_shot.setObjectName("screen_shot")
        self.gate_open = QtWidgets.QPushButton(self.frame_5)
        self.gate_open.setGeometry(QtCore.QRect(200, 20, 131, 51))
        self.gate_open.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 1px solid;\n"
"    border-radius: 6px;\n"
"    color: rgb(0,0, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(245, 245, 245);\n"
"    color: rgb(55, 55, 55);\n"
"\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(235, 235, 235);\n"
"}")
        self.gate_open.setObjectName("gate_open")
        self.horizontalLayout_6.addWidget(self.frame_5)
        self.frame_3 = QtWidgets.QFrame(self.frame_4)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 96))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.msg_event = QtWidgets.QLabel(self.frame_3)
        self.msg_event.setGeometry(QtCore.QRect(10, 50, 701, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.msg_event.setFont(font)
        self.msg_event.setObjectName("msg_event")
        self.label_camera = QtWidgets.QLabel(self.frame_3)
        self.label_camera.setGeometry(QtCore.QRect(10, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_camera.setFont(font)
        self.label_camera.setObjectName("label_camera")
        self.msg_name_camera = QtWidgets.QLabel(self.frame_3)
        self.msg_name_camera.setGeometry(QtCore.QRect(80, 10, 631, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.msg_name_camera.setFont(font)
        self.msg_name_camera.setObjectName("msg_name_camera")
        self.horizontalLayout_6.addWidget(self.frame_3)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addWidget(self.frame_4)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout_2.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.screen_shot.setText(_translate("MainWindow", "Снимок"))
        self.gate_open.setText(_translate("MainWindow", "Открыть"))
        self.msg_event.setText(_translate("MainWindow", "Нет событий"))
        self.label_camera.setText(_translate("MainWindow", "Камера:"))
        self.msg_name_camera.setText(_translate("MainWindow", "CAM-NONE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
