# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/untitled_browser.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1120, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(850, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(120, 590))
        self.frame.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame.setSizeIncrement(QtCore.QSize(150, 0))
        self.frame.setBaseSize(QtCore.QSize(150, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMinimumSize(QtCore.QSize(180, 50))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vl_buttons = QtWidgets.QVBoxLayout()
        self.vl_buttons.setContentsMargins(0, 0, -1, -1)
        self.vl_buttons.setObjectName("vl_buttons")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(158, 500))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 156, 498))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButton.setMinimumSize(QtCore.QSize(120, 68))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.vl_buttons.addWidget(self.scrollArea, 0, QtCore.Qt.AlignTop)
        self.but_update_cams = QtWidgets.QPushButton(self.frame_3)
        self.but_update_cams.setMinimumSize(QtCore.QSize(158, 44))
        self.but_update_cams.setMaximumSize(QtCore.QSize(158, 44))
        self.but_update_cams.setObjectName("but_update_cams")
        self.vl_buttons.addWidget(self.but_update_cams)
        self.verticalLayout_2.addLayout(self.vl_buttons)
        self.verticalLayout.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignTop)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(900, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(1, 9, 1, -1)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lab_cam_name = QtWidgets.QLabel(self.frame_2)
        self.lab_cam_name.setMaximumSize(QtCore.QSize(16777215, 15))
        self.lab_cam_name.setObjectName("lab_cam_name")
        self.verticalLayout_3.addWidget(self.lab_cam_name)
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_5 = QtWidgets.QFrame(self.page)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 504))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Frame_Gate_For_Hide = QtWidgets.QFrame(self.frame_5)
        self.Frame_Gate_For_Hide.setMaximumSize(QtCore.QSize(230, 16777215))
        self.Frame_Gate_For_Hide.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Frame_Gate_For_Hide.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame_Gate_For_Hide.setObjectName("Frame_Gate_For_Hide")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.Frame_Gate_For_Hide)
        self.verticalLayout_9.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_9.setSpacing(2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.Frame_Gate_Control = QtWidgets.QFrame(self.Frame_Gate_For_Hide)
        self.Frame_Gate_Control.setMinimumSize(QtCore.QSize(0, 0))
        self.Frame_Gate_Control.setMaximumSize(QtCore.QSize(220, 490))
        self.Frame_Gate_Control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Frame_Gate_Control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame_Gate_Control.setObjectName("Frame_Gate_Control")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.Frame_Gate_Control)
        self.verticalLayout_5.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gate_state_img = QtWidgets.QLabel(self.Frame_Gate_Control)
        self.gate_state_img.setMinimumSize(QtCore.QSize(218, 246))
        self.gate_state_img.setMaximumSize(QtCore.QSize(218, 246))
        self.gate_state_img.setText("")
        self.gate_state_img.setObjectName("gate_state_img")
        self.verticalLayout_5.addWidget(self.gate_state_img)
        self.frame_7 = QtWidgets.QFrame(self.Frame_Gate_Control)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_8 = QtWidgets.QFrame(self.frame_7)
        self.frame_8.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_8.setSpacing(1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.text_status = QtWidgets.QLabel(self.frame_8)
        self.text_status.setObjectName("text_status")
        self.verticalLayout_8.addWidget(self.text_status)
        self.verticalLayout_6.addWidget(self.frame_8)
        self.frame_9 = QtWidgets.QFrame(self.frame_7)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.bt_open_close = QtWidgets.QPushButton(self.frame_9)
        self.bt_open_close.setMinimumSize(QtCore.QSize(130, 40))
        self.bt_open_close.setObjectName("bt_open_close")
        self.verticalLayout_7.addWidget(self.bt_open_close)
        self.verticalLayout_6.addWidget(self.frame_9, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_5.addWidget(self.frame_7)
        self.verticalLayout_9.addWidget(self.Frame_Gate_Control)
        self.frame_10 = QtWidgets.QFrame(self.Frame_Gate_For_Hide)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_9.addWidget(self.frame_10)
        self.horizontalLayout_2.addWidget(self.Frame_Gate_For_Hide)
        self.lab_camera_img = QtWidgets.QLabel(self.frame_5)
        self.lab_camera_img.setText("")
        self.lab_camera_img.setObjectName("lab_camera_img")
        self.horizontalLayout_2.addWidget(self.lab_camera_img)
        self.verticalLayout_10.addWidget(self.frame_5)
        self.stackedWidget.addWidget(self.page)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gate_state_3 = QtWidgets.QLabel(self.page_3)
        self.gate_state_3.setMinimumSize(QtCore.QSize(400, 300))
        self.gate_state_3.setMaximumSize(QtCore.QSize(400, 300))
        self.gate_state_3.setText("")
        self.gate_state_3.setObjectName("gate_state_3")
        self.horizontalLayout_3.addWidget(self.gate_state_3)
        self.cam_img_3 = QtWidgets.QLabel(self.page_3)
        self.cam_img_3.setText("")
        self.cam_img_3.setObjectName("cam_img_3")
        self.horizontalLayout_3.addWidget(self.cam_img_3)
        self.stackedWidget.addWidget(self.page_3)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.lab_camera_img_2 = QtWidgets.QLabel(self.page_2)
        self.lab_camera_img_2.setText("")
        self.lab_camera_img_2.setObjectName("lab_camera_img_2")
        self.verticalLayout_11.addWidget(self.lab_camera_img_2)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout_3.addWidget(self.stackedWidget)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.warning_msg = QtWidgets.QLabel(self.frame_4)
        self.warning_msg.setGeometry(QtCore.QRect(0, 0, 591, 41))
        self.warning_msg.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.warning_msg.setFont(font)
        self.warning_msg.setText("")
        self.warning_msg.setObjectName("warning_msg")
        self.verticalLayout_3.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Test Button"))
        self.but_update_cams.setText(_translate("MainWindow", "Обновить"))
        self.lab_cam_name.setText(_translate("MainWindow", "Просмотр камеры: "))
        self.text_status.setText(_translate("MainWindow", "Нет данных"))
        self.bt_open_close.setText(_translate("MainWindow", "Открыть"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
