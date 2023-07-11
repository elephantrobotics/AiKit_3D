import cv2
import time
import numpy as np
from pymycobot.mycobot import MyCobot
from pymycobot.utils import get_port_list
from DepthSensor import get_depth,convert_depth_to_world
from RGBSensor import get_color


class Object_detect:
    def __init__(self,camera_x = 165, camera_y = 10, camera_z = 382):

        # 移动角度
        self.move_angles = [
            [-28.39, 45.87, -92.37, -41.3, 2.02, 9.58],  # init the point
            [-5.71, 24.6, -70.92, -38.49, -1.31, 130.34]  # point to grab
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
    def get_position(self, x, y,z):
        return y+self.camera_x, self.camera_y -x,self.camera_z - z

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
        self.mc = MyCobot(plist[0],115200)
        # 移动到初始位置
        self.mc.set_fresh_mode(0)
        self.mc.set_tool_reference([0, 0, 70, 0, 0, 0])

        self.mc.set_end_type(1)
        time.sleep(1)
        self.mc.send_angles(self.move_angles[0], 70)
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
        target_coords[2] = z+50
        print("target:", target_coords)
        time.sleep(1)
        self.mc.send_coords(target_coords, 80, 1)
        time.sleep(4)

        # 向下
        # self.mc.send_coord(3, z+30, 80)
        # time.sleep(1)
        print('z:', z)
        self.mc.send_coord(3, z, 80)
        time.sleep(4)
        # 打开吸泵
        self.pump_on()
        time.sleep(2)

        self.mc.send_coord(3, z + 80, 80)
        time.sleep(4)

        # 移动到盒子
        self.mc.send_angles(self.boxes_angle[id], 50)
        time.sleep(4)
        # 关闭吸泵
        self.pump_off()
        time.sleep(3)
        #  回到初始位置
        self.mc.send_angles(self.move_angles[0], 50)
        time.sleep(1)

if __name__ == "__main__":
    flag = 0
    while cv2.waitKey(1)<0:
        detect = Object_detect()
        detect.init_robot()
        # 获取RGB的像素坐标
        x,y,detect.color = get_color()
        print("color_coord:",(x,y))
        print("id:",detect.color)
        if (x,y) != (0,0):

            # 获取深度信息
            dpt_x,dpt_y,dpt_z = get_depth(x,y)
            print("depth_coord:",(dpt_x,dpt_y,dpt_z))
            if(dpt_x, dpt_y, dpt_z) != (0,0,0):
                detect.obj_relative_camera_x, detect.obj_relative_camera_y, detect.obj_relative_camera_z = convert_depth_to_world(x,y,dpt_z)
                print("camera_coord:",(detect.obj_relative_camera_x, detect.obj_relative_camera_y, detect.obj_relative_camera_z))
                grip_x, grip_y,grip_z = detect.get_position(detect.obj_relative_camera_x, detect.obj_relative_camera_y, detect.obj_relative_camera_z)
                print("grip_position:",grip_x,grip_y,grip_z)
                # 机械臂抓取
                detect.move(grip_x,grip_y,grip_z,detect.color)
                cv2.destroyAllWindows()
            else:
                print("no depth value!")
        else:
            print("nothing detected")