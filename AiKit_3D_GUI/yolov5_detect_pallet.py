#!/usr/bin/python
# -*- coding:utf-8 -*-
# @File    : yolov5_detect_pallet.py
# @Author  : Wang Weijian
# @Time    :  2023/07/31 15:53:35
# @function: the script is used to do something
# @version : V1

from multiprocessing import Process, Pipe
import cv2
import numpy as np
import threading
import os
import platform
import torch

class Object_detect():

    def __init__(self):
        # inherit the parent class
        super(Object_detect, self).__init__()

        # 目标框面积
        self.area = 0

        # yolov5 model file path
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.modelWeights = "./scripts/yolov5s.onnx"
        self.net = cv2.dnn.readNet(self.modelWeights)


        # Constants.
        self.SCORE_THRESHOLD = 0.15
        self.NMS_THRESHOLD = 0.15
        self.CONFIDENCE_THRESHOLD = 0.15
        self.label = None
        # 像素中心点
        self.x = 0
        self.y = 0

        '''加载类别名'''
        classesFile = "./scripts/coco.names"
        self.classes = None
        with open(classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')


    '''绘制类别'''
    # def draw_label(self, img, label, x, y):
    #     cv2.putText(img, label, (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

    '''
    预处理
    将图像和网络作为参数。
    - 首先，图像被转换为​​ blob。然后它被设置为网络的输入。
    - 该函数getUnconnectedOutLayerNames()提供输出层的名称。
    - 它具有所有层的特征，图像通过这些层向前传播以获取检测。处理后返回检测结果。
    '''

    def pre_process(self, input_image, net):
        blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (640,640), [0, 0, 0], 1,
                                     crop=False)
        # Sets the input to the network.
        net.setInput(blob)
        # Run the forward pass to get output of the output layers.
        outputs = net.forward(net.getUnconnectedOutLayersNames())
        return outputs

    '''后处理
    过滤 YOLOv5 模型给出的良好检测
    步骤
    - 循环检测。
    - 过滤掉好的检测。
    - 获取最佳班级分数的索引。
    - 丢弃类别分数低于阈值的检测。
    '''

    # detect object
    def post_process(self, input_image):
        class_ids = []
        confidences = []
        boxes = []
        blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (640,640), [0, 0, 0], 1,
                                     crop=False)
        # Sets the input to the network.
        self.net.setInput(blob)
        # Run the forward pass to get output of the output layers.
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())

        rows = outputs[0].shape[1]
        image_height, image_width = input_image.shape[:2]

        x_factor = image_width / 640
        y_factor = image_height / 640

        # 循环检测
        try:
            for r in range(rows):
                row = outputs[0][0][r]
                confidence = row[4]
                if confidence > self.CONFIDENCE_THRESHOLD:
                    classes_scores = row[5:]
                    class_id = np.argmax(classes_scores)
                    if (classes_scores[class_id] > self.SCORE_THRESHOLD):
                        confidences.append(confidence)
                        class_ids.append(class_id)
                        self.x,self.y, w, h = row[0], row[1], row[2], row[3]
                        left = int((self.x - w / 2) * x_factor)
                        top = int((self.y - h / 2) * y_factor)
                        width = int(w * x_factor)
                        height = int(h * y_factor)
                        box = np.array([left, top, width, height])
                        boxes.append(box)

                        '''非极大值抑制来获取一个标准框'''
                        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)

                        for i in indices:
                            box = boxes[i]
                            left = box[0]
                            top = box[1]
                            width = box[2]
                            height = box[3]
                            self.area = width*height

                            # 描绘标准框
                            cv2.rectangle(input_image, (left, top), (left + width, top + height),(0,0,255),
                                          2)

                            # 像素中心点
                            self.x = left + (width) // 2
                            self.y = top + (height) // 2

                            cv2.circle(input_image, (self.x, self.y),5, (0,0,255), 10)

                            # 检测到的类别
                            self.label = "{}:{:.2f}".format(self.classes[class_ids[i]], confidences[i])

        except Exception as e:
            print(e)
            exit(0)

        if self.x+self.y > 0:
            return self.x,self.y, input_image
        else:
            return None

