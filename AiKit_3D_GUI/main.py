#! /usr/bin/env pyhton3.9
# encoding:utf-8
import sys
import cv2
import numpy as np
import threading
import time
import traceback
import serial
import serial.tools.list_ports
from PyQt5 import QtCore
from PyQt5.Qt import *
from pymycobot.mycobot import MyCobot
from pymycobot.mycobotsocket import MyCobotSocket
from lib.AiKit_auto import Ui_AiKit_UI as AiKit_window
from camera import camera_Thread


class AiKit_APP(AiKit_window, QMainWindow, QWidget):
    def __init__(self):
        super(AiKit_APP, self).__init__()
        self.setupUi(self)
        self.language_btn.clicked.connect(self.set_language)  # set language
        self.comboBox_function.activated.connect(self.combox_func_checked)  # switch algorithm
        self.comboBox_port.highlighted.connect(self.get_serial_port_list)
        self.comboBox_port.activated.connect(self.get_serial_port_list)
        self.comboBox_device.highlighted.connect(self.set_device)
        self.comboBox_device.activated.connect(self.set_device)
        self.comboBox_baud.highlighted.connect(self.set_baud)
        self.comboBox_baud.activated.connect(self.set_baud)
        self.connect_btn.clicked.connect(self.robotics_connect)
        self.comboBox_function.highlighted.connect(self.choose_func)
        self.comboBox_function.activated.connect(self.choose_func)
        self.discern_btn.clicked.connect(self.start_detect)
        self.crawl_btn.clicked.connect(self.start_pick)
        self.current_coord_btn.clicked.connect(self.get_real_coords)
        self.image_coord_btn.clicked.connect(self.get_pixel_coords)
        self.open_camera_btn.clicked.connect(self.open_camera)
        self.M5 = ['myCobot 280 for M5', 'mechArm 270 for M5']  # M5 robot
        self.Pi = ['myCobot 280 for Pi', 'mechAm 270 for Pi']  # Pi robot
        self.port = self.comboBox_port.currentText()
        self.baud = None
        self.device = None
        self.mode = None
        self.detector = None
        self.robotics = None
        self.camera_x, self.camera_y, self.camera_z = 0, 0, 0  # 相机相对于机械臂的实际坐标
        self.real_x, self.real_y, self.real_z = 0, 0, 0
        self.port_list = []

        self.language = 1  # Control language, 1 is English, 2 is Chinese
        if self.language == 1:
            self.btn_color(self.language_btn, 'green')
        else:
            self.btn_color(self.language_btn, 'blue')
        self.is_language_btn_click = False

        self.init_ico()
        self._init_fun()
        self.combox_func_checked()

    def init_ico(self):
        """
        init UI interface ico
        """
        self.logo_lab.setPixmap(QPixmap('AiKit_UI_img/logo.ico'))
        self.logo_lab.setScaledContents(True)
        self.close_btn.setIcon(QIcon('AiKit_UI_img/close.ico'))
        self.max_btn.setIcon(QIcon('AiKit_UI_img/max.ico'))
        self.min_btn.setIcon(QIcon('AiKit_UI_img/min.ico'))

    def btn_color(self, btn, color):
        if color == 'red':
            btn.setStyleSheet("background-color: rgb(231, 76, 60);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")
        elif color == 'green':
            btn.setStyleSheet("background-color: rgb(39, 174, 96);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")
        elif color == 'blue':
            btn.setStyleSheet("background-color: rgb(41, 128, 185);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")

    def set_language(self):
        """
        设置语言
        """
        self.is_language_btn_click = True
        if self.language == 1:
            self.language = 2
            self.btn_color(self.language_btn, 'blue')
        else:
            self.language = 1
            self.btn_color(self.language_btn, 'green')
        self._init_language()
        self.combox_func_checked()
        self.is_language_btn_click = False

    def _init_language(self):
        """
        初始化语言
        """
        _translate = QtCore.QCoreApplication.translate
        if self.language == 1:
            if not self.is_language_btn_click:
                return
            self.camara_show.setText(_translate("AiKit_UI", "Camera"))
            if self.open_camera_btn.text() == '打开':
                self.open_camera_btn.setText(_translate("AiKit_UI", "Open"))
            else:
                self.open_camera_btn.setText(_translate("AiKit_UI", "Close"))
            self.connect_lab.setText(_translate("AiKit_UI", "Connection"))
            if self.connect_btn.text() == '连接':
                self.connect_btn.setText(_translate("AiKit_UI", "CONNECT"))
            else:
                self.connect_btn.setText(_translate("AiKit_UI", "DISCONNECT"))
            self.device_lab.setText(_translate("AiKit_UI", "Device"))
            self.baud_lab.setText(_translate("AiKit_UI", "Baud"))
            self.port_lab.setText(_translate("AiKit_UI", "Serial Port"))
            self.func_lab.setText(_translate("AiKit_UI", "Control"))
            self.to_origin_btn.setText(_translate("AiKit_UI", "Go"))
            self.func_lab_2.setText(_translate("AiKit_UI", "Homing"))
            self.func_lab_4.setText(_translate("AiKit_UI", "Recognition"))
            self.discern_btn.setText(_translate("AiKit_UI", "Run"))
            self.func_lab_5.setText(_translate("AiKit_UI", "Algorithm:"))
            self.crawl_btn.setText(_translate("AiKit_UI", "Run"))
            self.func_lab_7.setText(_translate("AiKit_UI", "Pick"))
            self.func_lab_9.setText(_translate("AiKit_UI", "Algorithm"))
            self.func_lab_10.setText(_translate("AiKit_UI", "Select"))
            self.comboBox_function.setItemText(0, _translate("AiKit_UI", "Color recognition"))
            self.comboBox_function.setItemText(1, _translate("AiKit_UI", "shape recognition"))
            self.comboBox_function.setItemText(2, _translate("AiKit_UI", "Keypoints"))
            self.comboBox_function.setItemText(3, _translate("AiKit_UI", "yolov5"))

            self.connect_lab_3.setText(_translate("AiKit_UI", "Display"))
            self.current_coord_btn.setText(_translate("AiKit_UI", "  current coordinates"))
            self.image_coord_btn.setText(_translate("AiKit_UI", "  image coordinates"))
            self.language_btn.setText(_translate("AiKit_UI", "简体中文"))
        else:
            self.camara_show.setText(_translate("AiKit_UI", "相机"))
            if self.is_language_btn_click:
                if self.open_camera_btn.text() == 'Open':
                    self.open_camera_btn.setText(_translate("AiKit_UI", "打开"))
                else:
                    self.open_camera_btn.setText(_translate("AiKit_UI", "关闭"))
            else:
                self.open_camera_btn.setText(_translate("AiKit_UI", "打开"))
            self.connect_lab.setText(_translate("AiKit_UI", "连接"))
            if self.is_language_btn_click:
                if self.connect_btn.text() == 'CONNECT':
                    self.connect_btn.setText(_translate("AiKit_UI", "连接"))
                else:
                    self.connect_btn.setText(_translate("AiKit_UI", "断开"))
            else:
                self.connect_btn.setText(_translate("AiKit_UI", "连接"))
            self.device_lab.setText(_translate("AiKit_UI", "设备"))
            self.baud_lab.setText(_translate("AiKit_UI", "波特率"))
            self.port_lab.setText(_translate("AiKit_UI", "串口"))
            self.func_lab.setText(_translate("AiKit_UI", "控制"))
            self.to_origin_btn.setText(_translate("AiKit_UI", "运行"))
            self.func_lab_2.setText(_translate("AiKit_UI", "初始点"))
            self.func_lab_4.setText(_translate("AiKit_UI", "识别"))
            self.discern_btn.setText(_translate("AiKit_UI", "运行"))
            self.func_lab_5.setText(_translate("AiKit_UI", "算法:"))
            self.crawl_btn.setText(_translate("AiKit_UI", "运行"))
            self.func_lab_7.setText(_translate("AiKit_UI", "抓取"))
            self.func_lab_9.setText(_translate("AiKit_UI", "算法"))
            self.func_lab_10.setText(_translate("AiKit_UI", "选择"))
            self.comboBox_function.setItemText(0, _translate("AiKit_UI", "颜色识别"))
            self.comboBox_function.setItemText(1, _translate("AiKit_UI", "形状识别"))
            self.comboBox_function.setItemText(2, _translate("AiKit_UI", "特征点识别"))
            self.comboBox_function.setItemText(3, _translate("AiKit_UI", "yolov5"))

            self.connect_lab_3.setText(_translate("AiKit_UI", "坐标显示"))
            self.current_coord_btn.setText(_translate("AiKit_UI", "  实时坐标"))
            self.image_coord_btn.setText(_translate("AiKit_UI", "  定位坐标"))
            self.language_btn.setText(_translate("AiKit_UI", "English"))

    def combox_func_checked(self):
        self.algorithm_lab.setText(self.comboBox_function.currentText())

    # 初始化
    def _init_fun(self):
        self.get_serial_port_list()

    def set_device(self):
        self.device = self.comboBox_device.currentText()

    def set_baud(self):
        self.baud = self.comboBox_baud.currentText()
        # 物体相对于机械臂的实际坐标

    def device_change(self):
        if self.device in self.M5:
            self.comboBox_baud.setCurrentText("115200")
        else:
            self.comboBox_baud.setCurrentText("1000000")

    # 识别算法切换
    def choose_func(self):
        self.mode = self.comboBox_function.currentText()

    # 机械臂连接
    def robotics_connect(self):
        self.device = self.comboBox_device.currentText()
        print(self.device)
        if self.device == 'mechArm 270 for M5':
            init = threading.Thread(target=self.init_270_M5)
            init.start()
        elif self.device == 'mechArm 270 for Pi':
            init = threading.Thread(target=self.init_270_Pi)
            init.start()
        elif self.device == 'myCobot 280 for M5':
            init = threading.Thread(target=self.init_280_M5)
            init.start()
        elif self.device == 'myCobot 280 for Pi':
            init = threading.Thread(target=self.init_280_Pi)
            init.start()

    def init_270_M5(self):
        self.port = self.comboBox_port.currentText()
        self.baud = self.comboBox_baud.currentText()
        self.camera_x, self.camera_y, self.camera_z = 165, 0, 382
        self.robotics = MyCobot(self.port, self.baud)
        print("finished")
        self.robotics.set_fresh_mode(0)
        self.robotics.set_tool_reference([0, 0, 80, 0, 0, 0])
        self.robotics.set_end_type(1)
        time.sleep(1)
        self.robotics.send_angles([-90, 0, 0, -0.08, 77.08, 4.83], 30)
        time.sleep(3)

    def init_270_Pi(self):
        self.camera_x, self.camera_y, self.camera_z = 150, -5, 370
        self.robotics = MyCobotSocket(self.port, self.baud)
        self.robotics.set_gpio_mode("BCM")
        self.robotics.set_gpio_out(20, "out")
        self.robotics.set_gpio_out(21, "out")
        self.robotics.set_fresh_mode(0)
        self.robotics.set_tool_reference([0, 0, 80, 0, 0, 0])
        self.robotics.set_end_type(1)
        time.sleep(1)
        self.robotics.send_angles([-90, 0, 0, -0.08, 77.08, 4.83], 30)
        time.sleep(3)

    def init_280_M5(self):
        self.camera_x, self.camera_y, self.camera_z = 165, 10, 382
        self.robotics = MyCobot(self.port, self.baud)
        self.robotics.set_fresh_mode(0)
        self.robotics.set_tool_reference([0, 0, 70, 0, 0, 0])
        self.robotics.set_end_type(1)
        time.sleep(1)
        self.robotics.send_angles([-28.39, 45.87, -92.37, -41.3, 2.02, 9.58], 30)
        time.sleep(3)

    def init_280_Pi(self):
        self.camera_x, self.camera_y, self.camera_z = 162, 8, 370
        self.robotics = MyCobot(self.port, self.baud)
        self.robotics.send_angles([-28.39, 45.87, -92.37, -41.3, 2.02, 9.58], 30)
        time.sleep(3)

    # 开始识别
    def start_detect(self):
        self.mode = self.comboBox_function.currentText()
        if self.mode:
            self.detector = camera_Thread(str(self.mode))
            self.detector.start()
            try:
                while True:
                    self.detector.run()
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

    # 相机线程
    def open_camera(self):
        try:
            camera = threading.Thread(target=self.show_camera)
            camera.start()
        except KeyboardInterrupt:
            pass

    def show_camera(self):
        self.show_camera_lab_rgb.show()
        self.show_camera_lab_depth.show()
        while True:
            rgb = self.detector.rgb_show
            depth = self.detector.depth_show
            rgb_show = QImage(rgb, rgb.shape[1], rgb.shape[0], QImage.Format_RGB888)
            depth_show = QImage(depth, depth.shape[1], depth.shape[0], QImage.Format_RGB888)
            pixmap_color = QPixmap(rgb_show)
            pixmap_color = pixmap_color.scaled(320, 240, Qt.KeepAspectRatio)
            self.show_camera_lab_rgb.setPixmap(pixmap_color)
            self.show_camera_lab_depth.setPixmap(QPixmap.fromImage(depth_show))
            time.sleep(0.5)

    # 机械臂开始动作
    def start_pick(self):
        if self.device == 'mechArm 270 for M5':
            move = threading.Thread(target=self.run_270_M5)
            move.start()
        elif self.device == 'mechArm 270 for Pi':
            move = threading.Thread(target=self.run_270_Pi)
            move.start()
        elif self.device == 'myCobot 280 for M5':
            move = threading.Thread(target=self.run_280_M5)
            move.start()
        elif self.device == 'myCobot 280 for Pi':
            move = threading.Thread(target=self.run_280_Pi)
            move.start()

    # 获取机械臂当前坐标
    def get_current_coords(self):
        current_coords = self.robotics.get_coords()
        while (len(current_coords) == 0):
            current_coords = self.robotics.get_coords()
            time.sleep(2)
        return current_coords

    # 获取物体相对于相机的实际坐标
    def get_pixel_coords(self):
        try:
            get_coord = threading.Thread(target=self.get_pixel)
            get_coord.start()
        except KeyboardInterrupt:
            pass

    def get_pixel(self):
        while True:
            x, y, z = np.round(self.detector.world_x, 2), np.round(self.detector.world_y, 2), self.detector.world_z
            self.img_coord_lab.setText("    X:" + str(x) + "    Y:" + str(y) + "    Z:" + str(z))
            time.sleep(0.5)

    # 获取物体相对于机械臂的实际坐标
    def get_real_coords(self):
        try:
            get_coord = threading.Thread(target=self.get_real)
            get_coord.start()
        except KeyboardInterrupt:
            pass

    def get_real(self):
        while True:
            self.real_x = np.round(self.camera_x + self.detector.world_y, 2)
            self.real_y = np.round(self.camera_y - self.detector.world_x, 2)
            self.real_z = np.round(self.camera_z - self.detector.world_z, 2)
            self.cuttent_coord_lab.setText(
                "    X:" + str(self.real_x) + "    Y:" + str(self.real_y) + "    Z:" + str(self.real_z))
            time.sleep(0.5)

    # 开启吸泵
    def pump_on(self):
        if self.device in self.M5:
            self.robotics.set_basic_output(2, 0)
            self.robotics.set_basic_output(5, 0)
        else:
            self.robotics.set_gpio_output(20, 0)
            self.robotics.set_gpio_output(21, 0)

    # 关闭吸泵
    def pump_off(self):
        if self.device in self.M5:
            self.robotics.set_basic_output(2, 1)
            self.robotics.set_basic_output(5, 1)
        else:
            self.robotics.set_gpio_output(20, 1)
            self.robotics.set_gpio_output(21, 1)

    def run_270_M5(self):
        initial_pos = [-90, 0, 0, -0.08, 77.08, 4.83]
        precatch_pos = [0, 0, 0, -1.23, 78.31, 4.65]
        box_angles = [
            [-50.37, 12.21, -7.03, 1.14, 56.62, 1.93],  # D Sorting area
            [-30.76, 48.33, -52.55, 0.61, 55.98, 1.75],  # C Sorting area
            [52.03, 23.55, -25.57, 0.87, 65, 1.66],  # A Sorting area
            [90.43, 20.21, -25.48, 0.17, 75, 1.66],  # B Sorting area
        ]
        self.robotics.send_angles(precatch_pos, 30)
        time.sleep(3)
        # 到达物体上方
        current_coords = self.get_current_coords()
        current_coords[0] = self.real_x
        current_coords[1] = self.real_y
        current_coords[2] = self.real_z + 50
        self.robotics.send_coords(current_coords, 80, 1)
        time.sleep(4)

        # 到达物体
        self.robotics.send_coord(3, self.real_z, 50)
        time.sleep(3)

        # 开启吸泵
        self.pump_on()
        time.sleep(3)
        # 抬起
        self.robotics.send_coord(3, self.real_z + 80, 80)
        time.sleep(3)
        # 移动到盒子
        self.robotics.send_angles(box_angles[self.detector.box_id], 50)
        time.sleep(3)
        # 关闭吸泵
        self.pump_off()
        time.sleep(3)
        # 回原点
        self.robotics.send_angles(initial_pos, 50)
        time.sleep(3)

    def run_270_Pi(self):
        initial_pos = [-90, 0, 0, -0.08, 77.08, 4.83]
        precatch_pos = [0, 0, 0, -1.23, 86.31, 4.65]
        box_angles = [
            [-50.37, 12.21, -7.03, 1.14, 56.62, 1.93],  # D Sorting area
            [-30.76, 48.33, -52.55, 0.61, 55.98, 1.75],  # C Sorting area
            [52.03, 23.55, -25.57, 0.87, 65, 1.66],  # A Sorting area
            [90.43, 20.21, -25.48, 0.17, 75, 1.66],  # B Sorting area
        ]
        self.robotics.send_angles(precatch_pos, 30)
        time.sleep(3)
        # 到达物体上方
        current_coords = self.get_current_coords()
        current_coords[0] = self.real_x
        current_coords[1] = self.real_y
        current_coords[2] = self.real_z + 50
        self.robotics.send_coords(current_coords, 80, 1)
        time.sleep(4)

        # 到达物体
        self.robotics.send_coord(3, self.real_z, 50)
        time.sleep(3)

        # 开启吸泵
        self.pump_on()
        time.sleep(3)
        # 抬起
        self.robotics.send_coord(3, self.real_z + 80, 80)
        time.sleep(3)
        # 移动到盒子
        self.robotics.send_angles(box_angles[self.detector.box_id], 50)
        time.sleep(3)
        # 关闭吸泵
        self.pump_off()
        time.sleep(3)
        # 回原点
        self.robotics.send_angles(initial_pos, 50)
        time.sleep(3)

    def run_280_M5(self):
        initial_pos = [-28.39, 45.87, -92.37, -41.3, 2.02, 9.58]
        precatch_pos = [-5.71, 24.6, -70.92, -38.49, -1.31, 130.34]
        box_angles = [
            [-30.4, -3.33, -118.21, 37.61, 3.69, 76.55],  # D Sorting area
            [-18.28, -72.07, 0.52, -7.03, 0, 87.01],  # C Sorting area
            [76.55, -14.76, -90.17, 19.16, 1.58, -45.52],  # A Sorting area
            [107.4, 0, -117.86, 34.71, 6.41, -21.7],  # B Sorting area
        ]
        self.robotics.send_angles(precatch_pos, 30)
        time.sleep(3)
        # 到达物体上方
        current_coords = self.get_current_coords()
        current_coords[0] = self.real_x
        current_coords[1] = self.real_y
        current_coords[2] = self.real_z + 50
        self.robotics.send_coords(current_coords, 80, 1)
        time.sleep(4)

        # 到达物体
        self.robotics.send_coord(3, self.real_z, 50)
        time.sleep(3)

        # 开启吸泵
        self.pump_on()
        time.sleep(3)
        # 抬起
        self.robotics.send_coord(3, self.real_z + 80, 80)
        time.sleep(3)
        # 移动到盒子
        self.robotics.send_angles(box_angles[self.detector.box_id], 50)
        time.sleep(3)
        # 关闭吸泵
        self.pump_off()
        time.sleep(3)
        # 回原点
        self.robotics.send_angles(initial_pos, 50)
        time.sleep(3)

    def run_280_Pi(self):
        initial_pos = [-28.39, 45.87, -92.37, -41.3, 2.02, 9.58]
        precatch_pos = [0, 45.87, -92.37, -41.3, 2.02, 9.58]
        box_angles = [
            [-30.4, -3.33, -118.21, 37.61, 3.69, 76.55],  # D Sorting area
            [-18.28, -72.07, 0.52, -7.03, 0, 87.01],  # C Sorting area
            [76.55, -14.76, -90.17, 19.16, 1.58, -45.52],  # A Sorting area
            [107.4, 0, -117.86, 34.71, 6.41, -21.7],  # B Sorting area
        ]
        self.robotics.send_angles(precatch_pos, 30)
        time.sleep(3)
        # 到达物体上方
        current_coords = self.get_current_coords()
        current_coords[0] = self.real_x
        current_coords[1] = self.real_y
        current_coords[2] = self.real_z + 50
        self.robotics.send_coords(current_coords, 80, 1)
        time.sleep(4)

        # 到达物体
        self.robotics.send_coord(3, self.real_z, 50)
        time.sleep(3)

        # 开启吸泵
        self.pump_on()
        time.sleep(3)
        # 抬起
        self.robotics.send_coord(3, self.real_z + 80, 80)
        time.sleep(3)
        # 移动到盒子
        self.robotics.send_angles(box_angles[self.detector.box_id], 50)
        time.sleep(3)
        # 关闭吸泵
        self.pump_off()
        time.sleep(3)
        # 回原点
        self.robotics.send_angles(initial_pos, 50)
        time.sleep(3)

    # 获取串口列表
    def get_serial_port_list(self):
        """Get the current serial port and map it to the serial port drop-down box"""
        plist = [
            str(x).split(" - ")[0].strip() for x in serial.tools.list_ports.comports()
        ]
        try:
            if not plist:
                if self.comboBox_port.currentText() == 'no port':
                    return
                self.comboBox_port.clear()
                self.comboBox_port.addItem('no port')
                self.port_list = []
                return
            else:
                if self.port_list != plist:
                    self.port_list = plist
                    self.comboBox_port.clear()
                    for p in plist:
                        self.comboBox_port.addItem(p)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        AiKit_window = AiKit_APP()
        AiKit_window.show()
    except Exception as e:
        print(e)
        e = traceback.format_exc()
        with open("error.txt", "w") as f:
            f.write(str(e))
    sys.exit(app.exec_())