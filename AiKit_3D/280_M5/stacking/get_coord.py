import cv2
from yolov5_detect import Object_detect


class Get_coord:
    def __init__(self,rgb,depth):
        self.rgb_data = rgb
        self.depth_data = depth
        self.detect_area = None
        self.pos = []
        self.grip_pos = None
        self.label = None
    def get_detect_area(self):
        if self.rgb_data is not None:
            # self.rgb_data = cv2.flip(self.rgb_data,0)
            # 限制识别区域
            roi = (250, 180, 130, 130)
            self.crop_x, self.crop_y, w, h = roi
            if roi != (0, 0, 0, 0):
                self.detect_area = self.rgb_data[self.crop_y:self.crop_y + h, self.crop_x:self.crop_x + w]

                cv2.imwrite('./res/yolov5_detect.png', self.detect_area)
    def get_pixel_coord(self):
        detector = Object_detect()
        self.get_detect_area()
        if self.detect_area is not None :
            detector.post_process(self.detect_area)

            if detector.area >= 1300 and detector.area < 2200:
                print("area:", detector.area)
                # print("no result")
            # else:
            # elif detector.label == 'suitcase' or detector.label == 'bottle' or detector.label == 'refrigerator':
        # if detector.label == 'suitcase' or detector.label == 'bottle':
                x = int(detector.x + self.crop_x)
                y = int(detector.y + self.crop_y)
                z = self.depth_data[int((y - 40) / 2), int((x - 40) / 2)]
                self.label = detector.label
                print("label:",self.label)
                print(type(self.label))
                print("pixel:",(x, y, z))
                self.pos.append([x,y,z])
            # cv2.putText(self.detect_area, self.label, (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
            # else:
            #     print('no result')

    def convert_depth_to_world(self,x, y, z):
        fx = 454.367
        fy = 454.367
        cx = 313.847
        cy = 239.89
        ratio = float(z / 1000)
        world_x = float((x - cx) * ratio) / fx
        world_x = world_x * 1000
        world_y = float((y - cy) * ratio) / fy
        world_y = world_y * 1000
        world_z = float(z)
        return world_x, world_y, world_z


    def get_world_coord(self):
        self.get_pixel_coord()
        if len(self.pos) != 0:
            self.pos.sort(key = lambda x:(x[2],x[0]),reverse= False)
            x,y,z = self.pos[0]
            x,y,z = self.convert_depth_to_world(x,y,z)
            print("world:",x,y,z)
            self.grip_pos = [x,y,z]
            # return grip_pos