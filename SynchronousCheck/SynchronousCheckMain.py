import os

import cv2
import numpy as np


class Stitcher:

    def get_M(self, images, ratio=0.75, reprojThresh=4.0):
        # 获取输入图片
        (long_focal_img, short_focal_img) = images
        (kps_long, featuresLong) = self.detectAndDescribe(long_focal_img)
        (kps_short, featuresShort) = self.detectAndDescribe(short_focal_img)
        M = self.matchKeypoints(kps_short, kps_long, featuresShort, featuresLong, ratio, reprojThresh)

        # 如果返回结果为空，没有匹配成功的特征点，退出算法
        if M is None:
            return None
        (matches, H, status) = M

        return H

    # 拼接函数
    def stitch(self, images, ratio=0.75, reprojThresh=4.0):
        (long_focal_img, short_focal_img) = images
        (matches, H, status) = self.get_M(images, ratio, reprojThresh)
        # 将图片A进行视角变换，result是变换后图片
        result = cv2.warpPerspective(short_focal_img, H,
                                     (short_focal_img.shape[1] + long_focal_img.shape[1], short_focal_img.shape[0]))
        result[0:long_focal_img.shape[0], 0:long_focal_img.shape[1]] = long_focal_img

        # 返回匹配结果
        return result

    def transformation(self, image, H):
        result = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
        return result

    def detectAndDescribe(self, image):
        descriptor = cv2.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(image, None)
        kps = np.float32([kp.pt for kp in kps])
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # 建立暴力匹配器
        matcher = cv2.BFMatcher()
        # 使用KNN检测来自A、B图的SIFT特征匹配对，K=2
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        for m in rawMatches:
            # print("3-0 {} m0:{} m1:{}".format(len(m), m[0].distance, m[1].distance))
            # 当最近距离跟次近距离的比值小于ratio值时，保留此匹配对
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                # 存储两个点在featuresA, featuresB中的索引值
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # 当筛选后的匹配对大于4时，计算视角变换矩阵
        if len(matches) > 4:
            # 获取匹配对的点坐标
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])
            # 计算视角变换矩阵
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            # 返回结果
            return (matches, H, status)
        # 如果匹配对小于4时，返回None
        return None

    def crop_image(self, img, ratio):
        wide = int(img.shape[1] * ratio)
        if ratio > 0:
            return img[:, 0:wide]
        else:
            return img[:, wide:]

    def mtx_similar(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        '''
        :param arr1:矩阵1
        :param arr2:矩阵2
        :return:相似度（0~1之间）
        '''
        if arr1.shape != arr2.shape:
            minx = min(arr1.shape[0], arr2.shape[0])
            miny = min(arr1.shape[1], arr2.shape[1])
            differ = arr1[:minx, :miny] - arr2[:minx, :miny]
        else:
            differ = arr1 - arr2
        dist = np.linalg.norm(differ, ord='fro')
        len1 = np.linalg.norm(arr1)
        len2 = np.linalg.norm(arr2)  # 普通模长
        denom = (len1 + len2) / 2
        similar = 1 - (dist / denom)
        return similar


def get_norm_mtx():
    stitcher = Stitcher()

    cm1 = r'./test_data/norm_data/cm1_.jpg'  # 5
    cm2 = r'./test_data/norm_data/cm2_.jpg'
    cm3 = r'./test_data/norm_data/cm3_.jpg'

    cm1 = cv2.imread(cm1)
    cm2 = cv2.imread(cm2)
    cm3 = cv2.imread(cm3)

    H_3_1 = stitcher.get_M([cm3, cm1])
    H_2_3 = stitcher.get_M([cm2, cm3])
    return H_3_1, H_2_3


# def main():
#     H_3_1_norm, H_2_3_norm = get_norm_mtx()
#     one_secen = 1000000000
#
#     cm1_base = r'C:\Users\NailinLiao\Desktop\test_data\cm1'
#     cm3_base = r'C:\Users\NailinLiao\Desktop\test_data\cm3'
#     cm1_list = os.listdir(cm1_base)
#     cm3_list = os.listdir(cm3_base)
#
#     for cm1_name in cm1_list:
#         cm1_img_path = os.path.join(cm1_base, cm1_name)
#         cm1 = cv2.imread(cm1_img_path)
#         ret = []
#         for cm3_name in cm3_list:
#             cm1_fram = int(str(cm1_name).split('.')[0])
#             cm3_fram = int(str(cm3_name).split('.')[0])
#             if abs(cm1_fram - cm3_fram) < one_secen / 3:
#                 cm3_img_path = os.path.join(cm3_base, cm3_name)
#                 cm3 = cv2.imread(cm3_img_path)
#                 H = get_True_H(cm3, cm1)
#                 similarity = mtx_similar3(H, H_3_1_norm)
#                 print(similarity)
#                 show_img(cm3, cm1)
#                 ret.append(similarity)
#
#         max_index = ret.index(max(ret))
#         print(cm1_name, cm3_list[max_index], max(ret))

def transformation_by_norm(images):
    (long_focal_img, short_focal_img) = images
    stitcher = Stitcher()
    H_3_1, H_2_3 = get_norm_mtx()
    long_focal_img = stitcher.crop_image(long_focal_img, 0.75)
    short_focal_img = stitcher.crop_image(short_focal_img, -0.75)
    result = stitcher.stitch([long_focal_img, short_focal_img])

    cv2.imshow('long_focal_img', long_focal_img)
    cv2.imshow('result', result)
    cv2.waitKey(0)


def test():
    short_focal_img = r'C:\Users\NailinLiao\Desktop\DataDevelopment\SynchronousCheck\test_data\test_data\cm1\1669342684066666690.jpg'
    long_focal_img = r'C:\Users\NailinLiao\Desktop\DataDevelopment\SynchronousCheck\test_data\test_data\cm3\1669342684066666690.jpg'
    long_focal_img = cv2.imread(long_focal_img)
    short_focal_img = cv2.imread(short_focal_img)

    transformation_by_norm([long_focal_img, short_focal_img])


if __name__ == '__main__':
    test()
