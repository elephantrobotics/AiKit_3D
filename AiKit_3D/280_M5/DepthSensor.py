from ObTypes import *
from Property import *
import Pipeline
import numpy as np
import cv2
import sys
from Error import ObException
from openni import _openni2 as c_api
# from openni.openni2 import convert_depth_to_world


def get_depth(x,y):
    dpt_x, dpt_y, dpt_z = 0,0,0

    try:
        pipe = Pipeline.Pipeline(None,None)
        config = Pipeline.Config()
        try:
            profiles = pipe.getStreamProfileList(OB_PY_SENSOR_DEPTH)
            # try:
            #     videoProfile = profiles.getVideoStreamProfile(640, 0, OB_PY_FORMAT_Y16, 30)
            # except ObException as e:
            #     print("未找到对应格式的Profile")
            videoProfile = profiles.getVideoStreamProfile(640, 0, OB_PY_FORMAT_UNKNOWN, 30)
            depthProfile = videoProfile.toConcreteStreamProfile(OB_PY_STREAM_VIDEO)
            config.enableStream(depthProfile)
        except ObException as e:
            print("当前设备不支持深度传感器！")
            sys.exit()

        pipe.start(config,None)

        if pipe.getDevice().isPropertySupported(OB_PY_PROP_DEPTH_MIRROR_BOOL,OB_PY_PERMISSION_WRITE):
            pipe.getDevice().setBoolProperty(OB_PY_PROP_DEPTH_MIRROR_BOOL,True)

        while True:
            frameSet = pipe.waitForFrames(100)
            if frameSet == None:
                continue
            else:
                depthFrame = frameSet.depthFrame()
                if depthFrame != None:
                    size = depthFrame.dataSize()
                    data = depthFrame.data()
                    if size:
                        data.resize((400,640,2))
                        dpt = data[:,:,0] + data[:,:,1]*256
                        dpt_x, dpt_y, dpt_z= x-40, y-40, dpt[y-40,x-40]
                        # print(dpt_x,dpt_y,dpt_z)
                        gray = dpt.astype(np.uint8)
                        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

                        # print("depth_pos:",(x-40,y-40,dpt[y-40,x-40]))
                        # print("world_pos:",(convert_depth_to_world(x-40,y-40,dpt[y-40,x-40])))
                        # world_x, world_y,world_z = convert_depth_to_world(config,x,y,dpt[y,x])
                        # print("real coord:",(world_x,world_y,world_z))
                        cv2.namedWindow("depthviewer",cv2.WINDOW_AUTOSIZE)
                        cv2.imshow("depthviewer",gray)

                        key = cv2.waitKey(1)
                        if key == ord('q'):
                            cv2.destroyWindow("depthviewer")
                            break
        pipe.stop()



    except ObException as e:
        print("Error!")
    return dpt_x, dpt_y, dpt_z


def convert_depth_to_world(x,y,z):
    fx = 454.367
    fy = 454.367
    cx = 313.847
    cy = 239.89
    ratio = float(z/1000)
    world_x = float((x - cx) * ratio) / fx
    world_x = world_x * 1000
    world_y = float((y - cy) * ratio) / fy
    world_y = world_y * 1000
    world_z = float(z)
    return world_x,world_y,world_z
