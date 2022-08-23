#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from hand_recognize.train_scratch import hand_recognize
from hand_detect.detect import hand_detect
from face_recognize.predict import face_recognize
from face_detect.face_detect import face_detect

from PyQt5.QtGui import QPalette, QBrush, QPixmap

import time
root_path = os.getcwd()
sys.path.insert(0, root_path+"/hand_detect") #这个后面的"/yolov5" 文件夹应该是指向的 yolov5根目录.

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # self.setBac
        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0


    def set_ui(self):
        font = QtGui.QFont()
        font.setFamily("kaiti")
        font.setPointSize(18)
        self.textBrowser = QtWidgets.QLabel("多重特征检测")
        self.textBrowser.setAlignment(Qt.AlignCenter)
        self.textBrowser.setFont(font)

        # self.label.setText(_translate("MainWindow", "TextLabel"))
        self.mm_layout = QVBoxLayout()
        self.l_down_widget = QtWidgets.QWidget()
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_cap = QtWidgets.QPushButton(u'拍照')
        self.det = QtWidgets.QPushButton(u'图片检测')
        self.text_browser = QTextBrowser(self)
        self.text_browser.setText("未进行检测")

        fontx = QtGui.QFont()
        fontx.setFamily("kaiti")
        fontx.setPointSize(16)

        # Button 的颜色修改
        button_color = [self.button_open_camera, self.button_cap, self.det, self.text_browser]
        for i in range(4):
            if 0 <= i <3:
                button_color[i].setFont(fontx)
                button_color[i].setStyleSheet("QPushButton{color:black}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{background-color:rgb(78,255,255)}"
                                              "QPushButton{border:2px}"
                                              "QPushButton{border-radius:10px}"
                                              "QPushButton{padding:2px 4px}")
            if i == 3:
                button_color[i].setFont(fontx)
                button_color[i].setStyleSheet("QTextBrowser{color:black}"
                                              "QTextBrowser{background-color:rgb(78,255,255)}"
                                              "QTextBrowser{border:2px}"
                                              "QTextBrowser{border-radius:10px}"
                                              "QTextBrowser{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_cap.setMinimumHeight(50)
        # self.text_browser.setFixedSize()
        self.det.setMinimumHeight(50)

        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_show_camera.setFixedSize(641, 481)
        # self.label_show_camera.setFixedSize(1300, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_cap)
        self.__layout_fun_button.addWidget(self.det)
        self.__layout_fun_button.addWidget(self.text_browser)
        self.__layout_fun_button.addWidget(self.label_move)
        # 添加一个右侧的组件
        self.right_widget = QWidget()
        self.right_widget_layout = QHBoxLayout()
        self.cap_label = QLabel()
        self.cap_label.setFixedSize(641, 481)

        self.cap_label.setAutoFillBackground(False)
        self.right_widget_layout.addWidget(self.label_show_camera)
        self.right_widget_layout.addWidget(self.cap_label)
        self.right_widget.setLayout(self.right_widget_layout)

        self.__layout_main.addWidget(self.right_widget)
        self.__layout_main.addLayout(self.__layout_fun_button)

        self.l_down_widget.setLayout(self.__layout_main)
        self.mm_layout.addWidget(self.textBrowser)
        self.mm_layout.addWidget(self.l_down_widget)
        self.setLayout(self.mm_layout)
        self.label_move.raise_()
        self.setWindowTitle(u'多重特征检测')

        '''
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''

    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_cap.clicked.connect(self.capx)
        self.det.clicked.connect(self.detect)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM,  cv2.CAP_DSHOW)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)

                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')

    def show_camera(self):
        flag, self.image = self.cap.read()
        # face = self.face_detect.align(self.image)
        # if face:
        #     pass
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        # show.shape[1] = 640, show.shape[0] = 480
        self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
        # self.x += 1
        # self.label_move.move(self.x,100)

        # if self.x ==320:
        #     self.label_show_camera.raise_()

    def capx(self):
        # FName = fr"images\cap{time.strftime('%Y%m%d%H%M%S', time.localtime())}"
        # cv2.imwrite(FName + ".jpg", self.image)
        # print(FName)
        # self.label_2.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.cap_label.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
        self.showImage.save("test.jpg", "JPG", 100)

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()

    def detect(self):
        self.my_thread = MyThread()  # 创建线程
        self.my_thread.start()  # 开始线程
        self.my_thread.finishSignal.connect(self.Change)

    def Change(self, msg):
        # print(msg)
        self.text_browser.setText(str(msg))


class MyThread(QThread):
    finishSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        hand_detect()
        face_detect()
        hand = hand_recognize()
        face = face_recognize()
        if hand == 0 and face < 1:
            self.finishSignal.emit(str('检测成功\n人脸:\n陈佳祺\n手势:\n布'))
        if face >= 1:
            self.finishSignal.emit(str('检测失败\n人脸:\n非陈佳祺'))
        if hand != 0:
            self.finishSignal.emit(str('检测失败\n手势:\n非布'))



if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    # ex.setStyleSheet("#MainWindow{border-image:url(DD.png)}")
    ex.show()
    App.exec_()