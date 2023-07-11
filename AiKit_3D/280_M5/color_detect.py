import numpy as np
import cv2
import math


class color_detector():
    def __init__(self):
        # inherit the parent class
        super(color_detector, self).__init__()
        self._color = None
        self.color_id = 0
        self.x,self.y = 0,0
        self.objectType = None
        self.theta = 0

    def color_detect(self,img):

        kernel = np.ones((5, 5), np.uint8)
        HSV_dist = {
            'red': {'Lower': np.array([0, 43, 46]), 'Upper': np.array([10, 255, 255])},
            'blue': {'Lower': np.array([78, 43, 46]), 'Upper': np.array([100, 255, 255])},
            'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([85, 255, 255])},
            'yellow': {"Lower": np.array([22, 93, 0]), "Upper": np.array([45, 255, 255])},
            # "cyan": {"Lower":np.array([78, 43, 46]),"Upper": np.array([99, 255, 255])},
        }

        if img is not None:

            # 高斯模糊
            gs = cv2.GaussianBlur(img, (5, 5), 0)
            # 转为 HSV
            hsv = cv2.cvtColor(gs, cv2.COLOR_BGR2HSV)

            erode = cv2.erode(hsv, None, iterations=2)
            for _color in HSV_dist:

                inRange_hsv = cv2.inRange(erode, HSV_dist[_color]['Lower'], HSV_dist[_color]['Upper'])
                # 腐蚀作用
                dilation = cv2.dilate(inRange_hsv, kernel, iterations=1)
                closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
                edges = cv2.Canny(closing, 10, 20)
                # 只检测外轮廓
                cnts, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                # print("cnts:",cnts)
                if len(cnts) > 0:
                    for cnt in cnts:
                        if cv2.contourArea(cnt) > 1500:
                            peri = cv2.arcLength(cnt, True)
                            # print("轮廓近似值：",peri)
                            """
                                    approxPolyDP函数是opencv中利用来对指定的点集进行逼近，其逼近的精度是可设置的对应的函数为：
                                    void approxPolyDP(InputArray curve, OutputArray approxCurve, double epsilon, bool closed)；

                                    例如：approxPolyDP(contourMat, approxCurve, 10, true);//找出轮廓的多边形拟合曲线

                                    第一个参数 InputArray curve：输入的点集
                                    第二个参数OutputArray approxCurve：输出的点集，当前点集是能最小包容指定点集的。画出来即是一个多边形；
                                    第三个参数double epsilon：指定的精度，也即是原始曲线与近似曲线之间的最大距离。
                                    第四个参数bool closed：若为true,则说明近似曲线是闭合的，反之，若为false，则断开。
                                    返回列表元素，每一个元素代表一个边沿信息
                            """
                            # 提取拐点
                            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                            # print('approx:',approx)
                            objCor = len(approx)

                            if objCor == 4:

                                # print('object_type:', objectType)
                                # 可旋转矩形，即最小的外包矩形
                                """
                                        函数 cv2.minAreaRect() 返回一个Box2D结构 rect：（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）。
                                        分别对应于返回值：(rect[0][0],  rect[0][1]),  (rect[1][0],  rect[1][1]),  rect[2]
                                """
                                rect = cv2.minAreaRect(cnt)
                                # 中心点坐标
                                pos_x = int(rect[0][0])
                                pos_y = int(rect[0][1])
                                self.x, self.y = pos_x, pos_y

                                # print(f"position:x = {pos_x}, y = {pos_y}")
                                self.theta = np.round(rect[2], 2)
                                box = cv2.boxPoints(rect)
                                box = np.intp(box)
                                # print(box)
                                # print("theta:", theta)
                                _pos = (pos_x, pos_y)
                                # 判断矩形是否为正方形
                                W = math.sqrt(
                                    math.pow((box[0][0] - box[1][0]), 2) + math.pow((box[0][1] - box[1][1]), 2))
                                H = math.sqrt(
                                    math.pow((box[0][0] - box[3][0]), 2) + math.pow((box[0][1] - box[3][1]), 2))
                                # 长宽比
                                aspRatio = W / float(H)
                                if aspRatio > 0.98 and aspRatio < 1.03:

                                    self.objectType = "Square"  # 正方形
                                else:
                                    self.objectType = "Rectangle"  # 长方形

                                cv2.circle(img, _pos, 1, (0, 0, 255), 2)
                                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

                            # 根据物体颜色进行分拣
                            if _color == 'red':
                                self._color = 'red'
                                self.color_id = 0
                                break
                            elif _color == 'green':
                                self._color = 'green'
                                self.color_id = 1
                                break
                            elif _color == 'blue':
                                self._color = 'blue'
                                self.color_id = 2
                            elif _color == 'cyan':
                                self._color = 'cyan'
                                self.color_id = 2
                                break
                            elif _color == 'yellow':
                                self._color = 'yellow'
                                self.color_id = 3
                                break
