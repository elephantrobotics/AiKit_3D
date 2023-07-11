import argparse
# import imutils
import cv2
import numpy as np
import math


class shape_detector:
    def __init__(self):
        # inherit the parent class
        super(shape_detector, self).__init__()
        self.shape_id = 0
        self.x, self.y = 0, 0
        self.shape = None
    def shape_detect(self,img):
        if img is not None:
            # 转为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


            # 阈值化
            thresh = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # 边缘检测
            edges = cv2.Canny(thresh,50,100)
            # 在阈值化图像中找到轮廓并初始化形状检测器
            cnts, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_NONE)
            if len(cnts)> 0:
                for cnt in cnts:
                    if cv2.contourArea(cnt) > 1000:
                        peri = cv2.arcLength(cnt, True)
                        # 提取拐点
                        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                        # print('approx:',approx)
                        objCor = len(approx)
                        # 如果形状是一个三角形，它将有3个顶点
                        if objCor == 3:
                            self.shape = "triangle"
                            self.shape_id = 0
                            mm = cv2.moments(cnt)
                            self.x = int(mm['m10'] / mm['m00'])
                            self.y = int(mm['m01'] / mm['m00'])
                            cv2.circle(img, (self.x,self.y), 1, (0, 0, 255), 2)
                            cv2.drawContours(img, [cnt], 0, (0, 0, 255), 2)
                        # 如果形状有4个顶点，它要么是正方形，要么是矩形
                        elif objCor == 4:
                            # 寻找最小外接矩阵的中心点
                            rect = cv2.minAreaRect(cnt)
                            # 中心点坐标
                            pos_x = int(rect[0][0])
                            pos_y = int(rect[0][1])
                            self.x, self.y = pos_x, pos_y
                            self.theta = np.round(rect[2], 2)
                            box = cv2.boxPoints(rect)
                            box = np.intp(box)
                            _pos = (pos_x, pos_y)
                            # 判断矩形是否为正方形
                            W = math.sqrt(
                                math.pow((box[0][0] - box[1][0]), 2) + math.pow((box[0][1] - box[1][1]), 2))
                            H = math.sqrt(
                                math.pow((box[0][0] - box[3][0]), 2) + math.pow((box[0][1] - box[3][1]), 2))
                            # 长宽比
                            aspRatio = W / float(H)
                            if aspRatio > 0.98 and aspRatio < 1.03:
                                self.shape = "Square"  # 正方形
                                self.shape_id = 1
                            else:
                                self.shape = "Rectangle"  # 长方形
                                self.shape_id = 2
                            cv2.circle(img, _pos, 1, (0, 0, 255), 2)
                            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

                        # 否则，我们假设形状是一个圆
                        elif objCor >= 5:
                            self.shape = "circle"
                            self.shape_id = 3
                            (self.x, self.y), radius = cv2.minEnclosingCircle(cnt)
                            center = (int(self.x), int(self.y))
                            radius = int(radius)
                            _font_x_pos = center[0]
                            _font_y_pos = center[1]
                            cv2.circle(img, center, 1, (0, 0, 255), 2)  # 绘制中心点
                            cv2.circle(img, center, radius, (0, 0, 255), 2)