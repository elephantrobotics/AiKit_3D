import cv2
import time
import numpy as np
from pymycobot.mycobot import MyCobot
from pymycobot.utils import get_port_list


# from camera import VideoStreamPipe


class Object_detect:
    def __init__(self, camera_x=162, camera_y=10, camera_z=382):

        # 移动角度
        self.move_angles = [
            [-28.39, 45.87, -92.37, -41.3, 2.02, 9.58],  # init the point
            # [21.88,10.28,-99.22,6.84,0.53,25.83],  # point to grab
            # [21.7,43.59,-132.53,5.53,0.61,25.57]
            # [5.53, 27.77, -153.28, 37.52, -0.17, 10.89]
            [4.92, 28.21, -133.76, 18.63, 0.17, 11.16]
        ]

        self.boxes_angle = [
            [-30.4, -3.33, -118.21, 37.61, 3.69, 76.55],  # D Sorting area
            [-18.28, -72.07, 0.52, -7.03, 0, 87.01],  # C Sorting area
            [76.55, -14.76, -90.17, 19.16, 1.58, -45.52],  # A Sorting area
            [107.4, 0, -117.86, 34.71, 6.41, -21.7],  # B Sorting area
        ]

        # 相机相对于机械臂底座的坐标
        self.camera_x, self.camera_y, self.camera_z = camera_x, camera_y, camera_z

        # 物体相对于相机的坐标
        self.obj_relative_camera_x, self.obj_relative_camera_y, self.obj_relative_camera_z = 0, 0, 0

        # 判断是否有物体存在
        self.flag = 1

        # 根据物体颜色选择放置的盒子
        self.color = 0

    # 计算物体和机械臂之间的坐标
    def get_position(self, x, y, z):
        return y + self.camera_x, self.camera_y - x, self.camera_z - z

    # 打开吸泵
    def pump_on(self):
        self.mc.set_basic_output(2, 0)
        self.mc.set_basic_output(5, 0)

    # 关闭吸泵
    def pump_off(self):
        self.mc.set_basic_output(2, 1)
        self.mc.set_basic_output(5, 1)

    def init_robot(self):
        plist = get_port_list()
        self.mc = MyCobot(plist[0], 115200)
        # 移动到初始位置
        self.mc.set_fresh_mode(0)
        self.mc.set_tool_reference([0, 0, 80, 0, 0, 0])

        self.mc.set_end_type(1)
        time.sleep(1)
        self.mc.send_angles(self.move_angles[0], 50)
        time.sleep(3)

    def move(self, x, y, z, id):
        # 移动到预备抓取位置
        self.mc.send_angles(self.move_angles[1], 50)
        time.sleep(3)
        self.deside_move(x, y, z, id)

    def get_current_coords(self):
        current_coords = self.mc.get_coords()
        while (len(current_coords) == 0):
            current_coords = self.mc.get_coords()
            # time.sleep(0.5)
        return current_coords

    def get_current_angles(self):
        current_angles = self.mc.get_angles()
        while (len(current_angles) == 0):
            current_angles = self.mc.get_angles()
            time.sleep(0.5)
        return current_angles

    def deside_move(self, x, y, z, id):

        # 移动到物体上方
        target_coords = self.get_current_coords().copy()
        # print('get_current_angles', self.get_current_angles())
        target_coords[0] = x
        target_coords[1] = y
        target_coords[2] = z + 30
        print("target:", target_coords)
        time.sleep(1)
        self.mc.send_coords(target_coords, 80, 1)
        time.sleep(2)

        # 向下
        # self.mc.send_coord(3, z+30, 80)
        # time.sleep(1)
        self.mc.send_coord(3, z, 40)
        time.sleep(3)
        # 打开吸泵
        self.pump_on()
        time.sleep(1)
        self.mc.send_coord(1, x + 5, 80)
        time.sleep(1)
        self.mc.send_coord(3, z + 80, 80)
        time.sleep(3)

        self.mc.send_coord(3, z + 80, 80)
        time.sleep(3)
        # 移动到盒子
        self.mc.send_angles(self.boxes_angle[id], 50)
        time.sleep(4)
        # 关闭吸泵
        self.pump_off()
        time.sleep(5)
        #  回到初始位置
        self.mc.send_angles(self.move_angles[0], 50)
        time.sleep(1)
