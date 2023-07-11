import numpy as np
import cv2,os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 读取储存特征数据的文件
def Get_npy(input_path):
    descriptors = []
    for (dirs, dirnames, filenames) in os.walk(input_path):
        for img_file in filenames:
            if img_file.endswith('npy'):
                descriptors.append(dirs+'/'+img_file)
    return descriptors

# 读取储存关键点信息的文件
def Get_txt(input_path):
    keypoints = []
    for (dirs, dirnames, filenames) in os.walk(input_path):
        for img_file in filenames:
            if img_file.endswith('txt'):
                keypoints.append(dirs+'/'+img_file)
    return keypoints

# 使用SIFT算法检查图像的关键点和描述符，创建FLANN匹配器
def SIFT_FLANN():
    sift = cv2.xfeatures2d.SIFT_create()
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=100)
    search_params = dict(checks=150)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    return sift,flann

# 检测并匹配
def Detect_Matches(sift,flann,query,descriptors,keypoints):
    query_gray = cv2.cvtColor(query,cv2.COLOR_BGR2GRAY)
    kps = []
    for txt in keypoints:
        lines = [line.strip() for line in open(txt)]
        for line in lines:
            list = line.split(',')
            kp = cv2.KeyPoint(x=float(list[0]), y=float(list[1]), size=float(list[2]), angle=float(list[3]),
                              response=float(list[4]), octave=int(list[5]), class_id=int(list[6]))
            kps.append(kp)
    # 寻找待查询图像的特征数据
    query_kp, query_ds = sift.detectAndCompute(query_gray, None)
    kp_query = cv2.drawKeypoints(query_gray, query_kp, None)
    plt.imshow(kp_query)
    plt.show()
    print("len:",len(query_kp))
    potential_culprits = {}

    points = []
    for desc in descriptors:
        good = []
        # 将图像query与特征数据文件的数据进行匹配
        matches = flann.knnMatch(query_ds, np.load(desc), k=2)
        # 清除错误匹配
        for m, n in matches:
            if m.distance < 0.8*n.distance:
                good.append(m)
                cnt = query_kp[m.queryIdx].pt
                points.append([int(cnt[0]), int(cnt[1])])
        print("img is %s ! matching rate is (%d)" % (desc, len(good)))
        potential_culprits[desc] = len(good)
    # 筛选匹配度最高的
    max_matches = None
    potential_suspect = None
    for culprit, matches in potential_culprits.items():
        if max_matches == None or matches > max_matches:
            max_matches = matches
            potential_suspect = culprit
    print("potential suspect is %s" % (((potential_suspect.replace("npy", "").split("/"))[-1].split("."))[0]))
    type = (((potential_suspect.replace("npy", "").split("/"))[-1].split("."))[0])
    box = ((potential_suspect.replace("npy", "").split("/"))[0]).split("\\")[-1]
    print(box)
    if box == 'A':
        box_id = 2
    elif box == 'B':
        box_id = 3
    elif box == 'C':
        box_id = 1
    elif box == 'D':
        box_id = 0
    center = center_coord(points).tolist()[0]
    center = [int(x) for x in center]
    print("中心特征点为", center)

    key = cv2.circle(query_gray, (center[0], center[1]), radius=10, color=(255, 0, 0), thickness=1)
    plt.imshow(key)
    plt.show()
    return center[0], center[1], type, box_id

# 获取中心特征点坐标
def center_coord(points):
    x = np.array(points)
    # 设定集群为1
    kmeans = KMeans(n_clusters=1, random_state=0).fit(x)
    return kmeans.cluster_centers_

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    _,frame = cap.read()
    print("请截取检测区域")
    print("Please capture the part of the detect area")
    # 选择ROI
    roi = cv2.selectROI(windowName="capture",
                        img=frame,
                        showCrosshair=False,
                        fromCenter=False)
    crop_x, crop_y, w, h = roi
    print(roi)
    if roi != (0, 0, 0, 0):
        crop = frame[crop_y:crop_y + h, crop_x:crop_x + w]
        keypoints = Get_txt('dataset')
        descriptors = Get_npy('dataset')
        sift, flann = SIFT_FLANN()
        x, y, type, id = Detect_Matches(sift, flann, crop, descriptors, keypoints)

        color_x = int(crop_x + x)
        color_y = int(crop_y + y)
        cv2.putText(frame, "type:" + str(type), (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255))
        cv2.putText(frame, "box_id:" + str(id), (20, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255))
        cv2.namedWindow("feature_detector", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("feature_detector", frame)
        key = cv2.waitKey(10)
        if input == ord('q'):
            cv2.destroyWindow("capture")