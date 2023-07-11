import numpy as np
from ObTypes import *
from Property import *
import Pipeline
import cv2
import sys
import Context
from Error import ObException
from detection import color_detect,circle_detect,Detector
from utli import *
from cube_gripper import Object_detect
from get_coord import Get_coord
class VideoStreamPipe:
    """
    视频流封装类
    """

    def __init__(self):
        self.real_x,self.real_y,self.real_z = 0,0,0
        try:
            # 创建一个Context，用于获取设备列表
            ctx = Context.Context(None)
            # 查询已经接入设备的列表
            devList = ctx.queryDeviceList()
            # 获取接入设备的数量
            devCount = devList.deviceCount()
            if devCount == 2:
                dev = devList.getDevice(1)
            # 创建一个Pipeline，Pipeline是整个高级API的入口，通过Pipeline可以很容易的打开和关闭
            # 多种类型的流并获取一组帧数据
                pipe = Pipeline.Pipeline(dev, None)
            else:
                pipe = Pipeline.Pipeline(None,None)
            self.pipe = pipe
            self.frame_time = 100

            # 通过创建Config来配置Pipeline要启用或者禁用哪些流
            config = Pipeline.Config()
            try:
                # 获取彩色相机的所有流配置，包括流的分辨率，帧率，以及帧的格式
                profiles = pipe.getStreamProfileList(OB_PY_SENSOR_COLOR)

                videoProfile = None
                try:
                    # 根据指定的格式查找对应的Profile,优先选择RGB888格式
                    videoProfile = profiles.getVideoStreamProfile(640,0,OB_PY_FORMAT_RGB888,30)
                except ObException as e:
                    # 没找到RGB888格式后不匹配格式查找对应的Profile进行开流
                    videoProfile = profiles.getVideoStreamProfile(640,0,OB_PY_FORMAT_UNKNOWN,30)
                    pass
                    print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" %(e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))

                colorProfile = videoProfile.toConcreteStreamProfile(OB_PY_STREAM_VIDEO)
                config.enableStream(colorProfile)
            except ObException as e:
                pass
                print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" %(e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))
                print("Current device is not support color sensor!")

            try:
                # 获取深度相机的所有流配置，包括流的分辨率，帧率，以及帧的格式
                profiles = pipe.getStreamProfileList(OB_PY_SENSOR_DEPTH)

                videoProfile = None
                try:
                    # 根据指定的格式查找对应的Profile,优先选择Y16格式
                    videoProfile = profiles.getVideoStreamProfile(320,0,OB_PY_FORMAT_Y16,30)
                except ObException as e:
                    # 没找到Y16格式后不匹配格式查找对应的Profile进行开流
                    videoProfile = profiles.getVideoStreamProfile(320,0,OB_PY_FORMAT_UNKNOWN,30)
                    pass
                    print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" %(e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))

                depthProfile = videoProfile.toConcreteStreamProfile(OB_PY_STREAM_VIDEO)
                config.enableStream(depthProfile)
            except ObException as e:
                print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" %(e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))
                print("Current device is not support depth sensor!")
                sys.exit()

            try:
                # 启动在Config中配置的流，如果不传参数，将启动默认配置启动流
                pipe.start(config, None)
                pipe.getDevice().setBoolProperty(OB_PY_PROP_COLOR_MIRROR_BOOL, False)
                pipe.getDevice().setBoolProperty(OB_PY_PROP_DEPTH_MIRROR_BOOL, False)
                pipe.getDevice().setBoolProperty(OB_PY_PROP_COLOR_AUTO_EXPOSURE_BOOL, False)
                pipe.getDevice().setBoolProperty(OB_PY_PROP_DEPTH_AUTO_EXPOSURE_BOOL, False)
            except ObException as e:
                pass
                print("function: %s\nargs: %s\nmessage: %s\ntype: %d\nstatus: %d" %(e.getName(), e.getArgs(), e.getMessage(), e.getExceptionType(), e.getStatus()))
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
                        newColorData = np.resize(newColorData,(colorHeight,colorWidth,3))
                        newColorData = cv2.cvtColor(newColorData,cv2.COLOR_BGR2RGB)
                        # newColorData = cv2.flip(newColorData,1)
                        # 将深度帧数据大小调整为(height,width,2)
                        depthData = np.resize(depthData, (depthHeight, depthWidth, 2))
                        depthData = depthData[:, :, 0] + depthData[:, :, 1] * 256
                        depthData = cv2.flip(depthData,1)
                        # 将深度帧数据16bit转8bit，用于渲染
                        newDepthData = ((depthData/500)*255).astype(np.uint8)
                        # 将深度帧数据GRAY转RGB
                        newDepthData = cv2.cvtColor(newDepthData, cv2.COLOR_GRAY2RGB)
                        newDepthData = cv2.flip(newDepthData,1)
                        return newColorData,depthData,newDepthData


if __name__ == "__main__":
    camera = VideoStreamPipe()
    gripper = Object_detect()
    gripper.init_robot()
    flag = 0
    while True:
        rgb,depth,depth_show = camera.camera()                            # 获得彩色图数据、深度图数据
        depth_flatten = depth[50:145,131:230].flatten()                                   # 深度数据展平
        # depth_flatten = depth.flatten()
        cv2.namedWindow("ColorViewer", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("DepthViewer", cv2.WINDOW_AUTOSIZE)
        bind_mouse_event(rgb,"ColorViewer",mouseHSV)
        get_coord = Get_coord(rgb,depth)
        get_coord.get_world_coord()                                       # 获得物体相对于相机的坐标
        rgb_show = cv2.flip(rgb,1)
        cv2.imshow("ColorViewer", rgb_show)

        cv2.imshow("DepthViewer", depth_show)
        if get_coord.detect_area is not None:
            cv2.imshow("detect_area",get_coord.detect_area)
        key = cv2.waitKey(1)
        if key == ord("q"):
            cv2.destroyAllWindows()
        if len(get_coord.pos) == 0:
            continue
        else:
            if flag == 4:
                flag = 0
            else:
                if get_coord.grip_pos is not None:
                    x,y,z = get_coord.grip_pos
                    if get_coord.label is not None:
                        if z > 370 or z == 0.0:                                                 # 没有深度值
                            pass
                        else:
                    #         pos_x, pos_y, pos_z = gripper.get_position(x, y, z)
                    #         print("task:", (pos_x, pos_y, pos_z))
                    #
                    #         gripper.move(pos_x, pos_y, pos_z, flag)
                    #         flag += 1
                    #
                    #         cv2.destroyAllWindows()
                    # else:
                    #     pass
                        # print("testing:",depth_flatten)
                        # for i in depth_flatten:
                            if 324 in depth_flatten or 325 in depth_flatten or 326 in depth_flatten:
                                if z < 330:
                                    pos_x, pos_y, pos_z = gripper.get_position(x, y, z)
                                else:
                                    continue
                            elif 344 in depth_flatten or 345 in depth_flatten or 342 in depth_flatten:
                                if z < 350:
                                    pos_x, pos_y, pos_z = gripper.get_position(x, y, z)
                                else:
                                    continue
                            elif 360 in depth_flatten or 361 in depth_flatten or 362 in depth_flatten:
                                if z < 370:
                                    pos_x, pos_y, pos_z = gripper.get_position(x, y, z)
                                else:
                                    continue
                            else:
                                continue
                            gripper.move(pos_x, pos_y, pos_z, flag)
                            print("task:", (pos_x, pos_y, pos_z))
                            flag += 1
                            cv2.destroyAllWindows()
                    #
                    # else:
                    #     pass


                        # elif 360 in depth_flatten:
                        #     if z < 370:
                        #         pos_x, pos_y, pos_z = gripper.get_position(x, y, z)
                        #     else:
                        #         break
                        # if pos_x:


    camera.pipe.stop()