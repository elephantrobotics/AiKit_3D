import threading

import Pipeline
import cv2
import sys
from Error import ObException
from ObTypes import *
from Property import *
import numpy as np
from color_detect import color_detector
from shape_detect import shape_detector
from yolov5_detect import Object_detect
from feature_detect import Detect_Matches, Get_npy, SIFT_FLANN, Get_txt


class camera_stream():
    def __init__(self):
        try:
            self.pipe = Pipeline.Pipeline(None, None)
            self.frame_time = 100

            # 通过创建Config来配置Pipeline要启用或者禁用哪些流
            config = Pipeline.Config()
            try:
                # 获取彩色相机的所有流配置，包括流的分辨率，帧率，以及帧的格式
                profiles = self.pipe.getStreamProfileList(OB_PY_SENSOR_COLOR)

                try:
                    # 根据指定的格式查找对应的Profile,优先选择RGB888格式
                    videoProfile = profiles.getVideoStreamProfile(640, 0, OB_PY_FORMAT_RGB888, 30)
                except ObException as e:
                    # 没找到RGB888格式后不匹配格式查找对应的Profile进行开流
                    videoProfile = profiles.getVideoStreamProfile(640, 0, OB_PY_FORMAT_UNKNOWN, 30)
                    pass
                    print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" % (
                        e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))

                colorProfile = videoProfile.toConcreteStreamProfile(OB_PY_STREAM_VIDEO)
                config.enableStream(colorProfile)
            except ObException as e:
                pass
                print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" % (
                    e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))
                print("Current device is not support color sensor!")

            try:
                # 获取深度相机的所有流配置，包括流的分辨率，帧率，以及帧的格式
                profiles = self.pipe.getStreamProfileList(OB_PY_SENSOR_DEPTH)

                try:
                    # 根据指定的格式查找对应的Profile,优先选择Y16格式
                    videoProfile = profiles.getVideoStreamProfile(320, 0, OB_PY_FORMAT_Y16, 30)
                except ObException as e:
                    # 没找到Y16格式后不匹配格式查找对应的Profile进行开流
                    videoProfile = profiles.getVideoStreamProfile(320, 0, OB_PY_FORMAT_UNKNOWN, 30)
                    pass
                    print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" % (
                        e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))

                depthProfile = videoProfile.toConcreteStreamProfile(OB_PY_STREAM_VIDEO)
                config.enableStream(depthProfile)
            except ObException as e:
                print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" % (
                    e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))
                print("Current device is not support depth sensor!")
                sys.exit()

            try:
                # 启动在Config中配置的流，如果不传参数，将启动默认配置启动流
                self.pipe.start(config, None)
                self.pipe.getDevice().setBoolProperty(OB_PY_PROP_COLOR_MIRROR_BOOL, False)
                self.pipe.getDevice().setBoolProperty(OB_PY_PROP_DEPTH_MIRROR_BOOL, False)
                self.pipe.getDevice().setBoolProperty(OB_PY_PROP_COLOR_AUTO_EXPOSURE_BOOL, False)
                self.pipe.getDevice().setBoolProperty(OB_PY_PROP_DEPTH_AUTO_EXPOSURE_BOOL, False)
            except ObException as e:
                pass
                print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" % (
                    e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))
        except ObException as e:
            pass
            print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" % (
                e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))

    def camera(self):
        while True:
            frame = self.pipe.waitForFrames(self.frame_time)
            if frame is not None:
                colorFrame = frame.colorFrame()
                depthFrame = frame.depthFrame()
                if colorFrame != None and depthFrame != None:
                    colorSize = colorFrame.dataSize()
                    colorData = colorFrame.data()
                    depthSize = depthFrame.dataSize()
                    depthData = depthFrame.data()
                    colorWidth = colorFrame.width()
                    colorHeight = colorFrame.height()
                    depthWidth = depthFrame.width()
                    depthHeight = depthFrame.height()
                    if colorSize != 0 and depthSize != 0:
                        newColorData = colorData
                        newColorData = np.resize(newColorData, (colorHeight, colorWidth, 3))
                        newColorData = cv2.cvtColor(newColorData, cv2.COLOR_BGR2RGB)
                        # newColorData = cv2.flip(newColorData,1)
                        # 将深度帧数据大小调整为(height,width,2)
                        depthData = np.resize(depthData, (depthHeight, depthWidth, 2))
                        depthData = depthData[:, :, 0] + depthData[:, :, 1] * 256
                        depthData = cv2.flip(depthData, 1)
                        # 将深度帧数据16bit转8bit，用于渲染
                        newDepthData = ((depthData / 500) * 255).astype(np.uint8)
                        # 将深度帧数据GRAY转RGB
                        newDepthData = cv2.cvtColor(newDepthData, cv2.COLOR_GRAY2RGB)
                        newDepthData = cv2.flip(newDepthData, 1)
                        return newColorData, depthData, newDepthData


class camera_Thread(threading.Thread):
    def __init__(self, detector):
        threading.Thread.__init__(self)
        self.camera = camera_stream()
        self.rgb_show = None
        self.rgb_data = None
        self.depth_show = None
        self.depth_data = None
        self.detector = detector
        self.pixel_x, self.pixel_y, self.pixel_z = 0, 0, 0
        self.world_x, self.world_y, self.worlf_z = 0, 0, 0
        self.box_id = 0
        self.world_z = 0

    def get_camera_frame(self):
        self.rgb_data, self.depth_data, self.depth_show = self.camera.camera()
        self.rgb_show = cv2.flip(self.rgb_data, 1)
        self.rgb_show = cv2.cvtColor(self.rgb_show, cv2.COLOR_BGR2RGB)

    def get_pixel_coord(self, detector):
        if detector == 'Color recognition':
            roi = (230, 145, 176, 175)
            crop_x, crop_y, w, h = roi
            crop = self.rgb_data[crop_y:crop_y + h, crop_x:crop_x + w]
            color_detect = color_detector()
            color_detect.color_detect(crop)
            if color_detect.x:
                color_detect.x = int(crop_x + color_detect.x)
                color_detect.y = int(crop_y + color_detect.y)
                self.pixel_x, self.pixel_y = color_detect.x, color_detect.y
                self.box_id = color_detect.color_id

        elif detector == 'Shape recognition':
            roi = (230, 145, 176, 175)
            crop_x, crop_y, w, h = roi
            crop = self.rgb_data[crop_y:crop_y + h, crop_x:crop_x + w]
            shape_detect = shape_detector()
            shape_detect.shape_detect(crop)
            if shape_detect.x:
                shape_detect.x = int(crop_x + shape_detect.x)
                shape_detect.y = int(crop_y + shape_detect.y)
                self.pixel_x, self.pixel_y = shape_detect.x, shape_detect.y
                self.box_id = shape_detect.shape_id
        elif detector == 'Keypoints':
            roi = cv2.selectROI(windowName="capture",
                                img=self.rgb_data,
                                showCrosshair=False,
                                fromCenter=False)
            crop_x, crop_y, w, h = roi
            print(roi)
            if roi != (0, 0, 0, 0):
                crop = self.rgb_data[crop_y:crop_y + h, crop_x:crop_x + w]
                keypoints = Get_txt('dataset')
                descriptors = Get_npy('dataset')
                sift, flann = SIFT_FLANN()
                x, y, type, self.box_id = Detect_Matches(sift, flann, crop, descriptors, keypoints)
                color_x = int(crop_x + x)
                color_y = int(crop_y + y)
                self.pixel_x, self.pixel_y = color_x, color_y
        elif detector == 'yolo v5':
            roi = (230, 145, 176, 175)
            crop_x, crop_y, w, h = roi
            crop = self.rgb_data[crop_y:crop_y + h, crop_x:crop_x + w]
            cv2.imwrite('./res/yolov5_detect.png', crop)
            yolov5_detect = Object_detect()
            yolov5_detect.post_process(crop)
            if yolov5_detect.x:
                yolov5_detect.x = int(yolov5_detect.x + crop_x)
                yolov5_detect.y = int(yolov5_detect.y + crop_y)
                self.pixel_x, pixel_y = yolov5_detect.x, yolov5_detect.y
                self.box_id = 0

    def get_depth(self):
        if (self.pixel_x, self.pixel_y) != (0, 0):
            self.pixel_z = self.depth_data[int((self.pixel_y - 40) / 2), int((self.pixel_x - 40) / 2)]

    # 像素坐标转为物体相对于相机的实际坐标
    def convert_depth_to_world(self):
        fx = 454.367
        fy = 454.367
        cx = 313.847
        cy = 239.89

        ratio = float(self.pixel_z / 1000)
        world_x = float((self.pixel_x - cx) * ratio) / fx
        self.world_x = world_x * 1000

        world_y = float((self.pixel_y - cy) * ratio) / fy
        self.world_y = world_y * 1000

        self.world_z = float(self.pixel_z)

    def run(self):
        while True:
            self.get_camera_frame()
            self.get_pixel_coord(self.detector)
            if self.pixel_x != 0:
                self.get_depth()
                if self.pixel_z != 0:
                    self.convert_depth_to_world()
                    self.pixel_x, self.pixel_y, self.pixel_z = 0, 0, 0
                    # print("x,y,z:", (self.world_x, self.world_y, self.world_z))

            # cv2.imshow("rgb_show",cv2.cvtColor(self.rgb_show,cv2.COLOR_BGR2RGB))
            # cv2.imshow("depth_show",self.depth_show)
            cv2.waitKey(1)

        self.camera.pipe.stop()


if __name__ == '__main__':
    # camera = camera_Thread('Color recognition')
    # camera.run()
    pass
