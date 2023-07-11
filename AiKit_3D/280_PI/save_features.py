import cv2
import numpy as np
import os


def get_img(input_path):
    image_paths = []
    for (dirs, dirnames, filenames) in os.walk(input_path):
        for img_file in filenames:
            ext = ['.jpg','.png','.jpeg','.tif']
            if img_file.endswith(tuple(ext)):
                image_paths.append(dirs+'/'+img_file)
    return image_paths

def SIFT_FLANN():
    sift = cv2.xfeatures2d.SIFT_create()
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=100)
    search_params = dict(checks=150)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    return sift,flann

def save_descriptor(sift,image_path):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = sift.detectAndCompute(img_gray, None)

    # 设置文件名并将特征数据保存到npy文件
    descriptor_file = image_path.replace(image_path.split('.')[-1], "npy")
    np.save(descriptor_file, descriptors)

def save_keypoints(sift,image_path):
    keypoints_file = image_path.replace(image_path.split('.')[-1], "txt")
    f = open(keypoints_file,"w")
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = sift.detectAndCompute(img_gray,None)
    for point in keypoints:
        p = str(point.pt[0]) + "," + str(point.pt[1]) + "," + str(point.size) + "," + str(point.angle) + "," + str(
            point.response) + "," + str(point.octave) + "," + str(point.class_id) + "\n"
        f.write(p)
    f.close()

if __name__=='__main__':
    input_path = 'dataset'
    image_paths = get_img(input_path)
    sift, flann = SIFT_FLANN()
    for image_path in image_paths:
        save_descriptor(sift, image_path)
        save_keypoints(sift,image_path)
    print('done!')
