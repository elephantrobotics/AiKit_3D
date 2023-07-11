from ObTypes import *
from Property import *
import Pipeline
import cv2
import sys
from Error import ObException
from color_detect import color_detector
from shape_detect import shape_detector
from yolov5_detect import Object_detect
from feature_detect import Detect_Matches,Get_npy,SIFT_FLANN,Get_txt
# from aruco_detect import aruco_detector

import warnings
warnings.filterwarnings('ignore')





def get_color():
    box = 0
    try:
        # 创建一个Pipeline，Pipeline是整个高级API的入口，通过Pipeline可以很容易的打开和关闭
        # 多种类型的流并获取一组帧数据
        pipe = Pipeline.Pipeline(None,None)
        # 通过创建Config来配置Pipeline要启用或者禁用哪些流
        config = Pipeline.Config()
        windowsWidth = 640
        windowsHeight = 480
        try:
            # 获取彩色相机的所有流配置，包括流的分辨率，帧率，以及帧的格式
            profiles = pipe.getStreamProfileList(OB_PY_SENSOR_COLOR)
            videoProfile = None
            try:
                # 根据指定的格式查找对应的Profile,优先选择RGB888格式
                videoProfile = profiles.getVideoStreamProfile(640, 0, OB_PY_FORMAT_RGB888, 30)
            except ObException as e:
                print("No profile found!")
                # 没找到RGB888格式后不匹配格式查找对应的Profile进行开流
                videoProfile = profiles.getVideoStreamProfile(640, 0, OB_PY_FORMAT_UNKNOWN, 30)
            colorProfile = videoProfile.toConcreteStreamProfile(OB_PY_STREAM_VIDEO)
            windowsWidth = colorProfile.width()
            windowsHeight = colorProfile.height()

            config.enableStream(colorProfile)
        except ObException as e:
            print("Current device is not support color sensor!")
            sys.exit()
        # pipe.set(CV_CAP_PROP_EXPOSURE, 156)
        # 启动在Config中配置的流，如果不传参数，将启动默认配置启动流
        pipe.start(config,None)
        params = pipe.getConfig()
        # 获取镜像属性是否有可写的权限
        if pipe.getDevice().isPropertySupported(OB_PY_PROP_DEPTH_MIRROR_BOOL,OB_PY_PERMISSION_WRITE):
            # 设置镜像
            pipe.getDevice().setBoolProperty(OB_PY_PROP_COLOR_AUTO_EXPOSURE_BOOL,False)
            pipe.getDevice().setBoolProperty(OB_PY_PROP_DEPTH_MIRROR_BOOL,True)
        print("请将可识别物体放置摄像头窗口进行拍摄")
        print("Please place an identifiable object in the camera window for shooting")
        print("*  热键(请在摄像头的窗口使用):                     *")
        print("*  hotkey(please use it in the camera window): *")
        print("*  a: 颜色识别(color detection)                  *")
        print("*  b: 形状识别(shape detection)                  *")
        print("*  c: 特征点识别(feature detection)               *")
        print("*  d: 物体识别(object detection)                  *")
        print("*  q: 退出(quit)                                 *")
        while True:
            # 以阻塞的方式等待一帧数据，该帧是一个复合帧，里面包含配置里启用的所有流的帧数据，
            # 并设置帧的等待超时时间为100ms
            frameSet = pipe.waitForFrames(100)

            if frameSet == None:
                continue
            else:
                # 在窗口中渲染一组帧数据，这里只渲染彩色帧
                rgbFrame = frameSet.colorFrame()
                if rgbFrame != None:
                    # 获取帧的大小和数据
                    size = rgbFrame.dataSize()
                    data = rgbFrame.data()
                    if size != 0:
                        rgb = data
                        # 将帧数据大小调整为(height,width,3)
                        rgb.resize((windowsHeight,windowsWidth,3))
                        # rgb.set(CV_CAP_PROP_EXPOSURE,156.0)
                        # 将帧数据BGR转RGB
                        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
                        # 创建窗口
                        cv2.namedWindow("RGBViewer", cv2.WINDOW_AUTOSIZE)
                        # 显示图像
                        cv2.imshow("RGBViewer", rgb)

                        input = cv2.waitKey(1) & 0xFF
                        if input == ord('q'):
                            print('quit')
                            break
                        elif input == ord('j'):
                            cv2.imwrite("./test.jpg", rgb)
                            break
                        # 颜色识别
                        elif input == ord('a'):
                            roi = (250, 180, 130, 130)
                            crop_x, crop_y, w, h = roi
                            if roi != (0, 0, 0, 0):
                                crop = rgb[crop_y:crop_y + h, crop_x:crop_x + w]
                            color_detect = color_detector()
                            color_detect.color_detect(crop)
                            if color_detect.x:
                                color_detect.x = int(crop_x + color_detect.x)
                                color_detect.y = int(crop_y + color_detect.y)
                                cv2.putText(rgb, "color:" + str(color_detect._color), (20, 20),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                cv2.putText(rgb, "shape:" + str(color_detect.objectType), (20, 40),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                cv2.putText(rgb, "coordinate:" + str((color_detect.x, color_detect.y)), (20, 60),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                                cv2.putText(rgb, "angle:" + str(color_detect.theta), (20, 80),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                cv2.putText(rgb, "color_id:" + str(color_detect.color_id), (20, 100),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                cv2.namedWindow("color_detector")
                                cv2.imshow("color_detector", rgb)
                                cv2.waitKey(10)
                                return color_detect.x, color_detect.y, color_detect.color_id
                                if input == ord('q'):
                                    cv2.destroyWindow("color_detector")
                            else:
                                cv2.putText(rgb, str("no result"), (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                            (0, 0, 255))
                                cv2.imshow('detect_result', rgb)
                                cv2.waitKey(10)
                                if input == ord('q'):
                                    cv2.destroyWindow("detect_result")
                        # 形状识别
                        elif input == ord('b'):
                            roi = (250, 180, 130, 130)
                            crop_x, crop_y, w, h = roi
                            if roi != (0, 0, 0, 0):
                                crop = rgb[crop_y:crop_y + h, crop_x:crop_x + w]
                            shape_detect = shape_detector()
                            shape_detect.shape_detect(crop)
                            if shape_detect.x:
                                shape_detect.x = int(crop_x + shape_detect.x)
                                shape_detect.y = int(crop_y + shape_detect.y)
                                cv2.putText(rgb, "shape:" + str(shape_detect.shape), (20, 20),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                cv2.putText(rgb, "coordinate:" + str((shape_detect.x, shape_detect.y)), (20, 40),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                                cv2.putText(rgb, "shape_id:" + str(shape_detect.shape_id), (20, 60),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                cv2.namedWindow("shape_detector")
                                cv2.imshow("shape_detector", rgb)
                                cv2.waitKey(10)
                                return shape_detect.x, shape_detect.y, shape_detect.shape_id
                                if input == ord('q'):
                                    cv2.destroyWindow("shape_detector")
                            else:
                                cv2.putText(rgb, str("no result"), (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                            (0, 0, 255))
                                cv2.imshow('detect_result', rgb)
                                cv2.waitKey(10)
                                if input == ord('q'):
                                    cv2.destroyWindow("detect_result")
                        # 特征识别
                        elif input == ord('c'):
                            print("请截取检测区域")
                            print("Please capture the part of the detect area")
                            # 选择ROI
                            roi = cv2.selectROI(windowName="capture",
                                                img=rgb,
                                                showCrosshair=False,
                                                fromCenter=False)
                            crop_x, crop_y, w, h = roi
                            print(roi)
                            if roi != (0, 0, 0, 0):
                                crop = rgb[crop_y:crop_y + h, crop_x:crop_x + w]
                                keypoints = Get_txt('dataset')
                                descriptors = Get_npy('dataset')
                                sift, flann = SIFT_FLANN()
                                x,y,type,id = Detect_Matches(sift, flann, crop, descriptors,keypoints)

                                color_x = int(crop_x + x)
                                color_y = int(crop_y + y)
                                cv2.putText(rgb, "type:" + str(type), (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                            (0, 0, 255))
                                cv2.putText(rgb, "box_id:" + str(id), (20, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                            (0, 0, 255))
                                cv2.namedWindow("feature_detector", cv2.WINDOW_AUTOSIZE)
                                cv2.imshow("feature_detector", rgb)
                                key = cv2.waitKey(10)
                                return color_x,color_y,id
                                if input == ord('q'):
                                    cv2.destroyWindow("capture")

                        # yolov5检测
                        elif input == ord('d'):
                            roi = (250, 180, 130, 130)
                            crop_x, crop_y, w, h = roi
                            if roi != (0, 0, 0, 0):
                                crop = rgb[crop_y:crop_y + h, crop_x:crop_x + w]
                                cv2.imwrite('./res/yolov5_detect.png', crop)
                                yolov5_detector = Object_detect()
                                yolov5_detector.post_process(crop)
                                if yolov5_detector.x:
                                    yolov5_detector.x = int(yolov5_detector.x + crop_x)
                                    yolov5_detector.y= int(yolov5_detector.y + crop_y)
                                    print((yolov5_detector.x,yolov5_detector.y))
                                    cv2.putText(rgb, yolov5_detector.label, (20,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                                    cv2.imshow('detect_result', rgb)
                                    cv2.waitKey(10)
                                    return yolov5_detector.x, yolov5_detector.y, 0
                                    if input == ord('q'):
                                        cv2.destroyWindow("detect_result")
                                else:
                                    cv2.putText(rgb, str("no result"), (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (0, 0, 255))
                                    cv2.imshow('detect_result', rgb)
                                    cv2.waitKey(10)
                                    if input == ord('q'):
                                        cv2.destroyWindow("detect_result")
        # 停止Pipeline，将不再产生帧数据
        pipe.stop()
    except ObException as e:
        print("Error!")
if __name__ == "__main__":
    get_color()