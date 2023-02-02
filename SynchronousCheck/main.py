import os
import cv2
import numpy as np
import time


class Stitcher:

    def get_M(self, images, ratio=0.75, reprojThresh=4.0):
        # 获取输入图片
        (long_focal_img, short_focal_img) = images
        long_focal_img = self.crop_image(long_focal_img, 0.75)
        short_focal_img = self.crop_image(short_focal_img, -0.75)
        (kps_long, featuresLong) = self.detectAndDescribe(long_focal_img)
        (kps_short, featuresShort) = self.detectAndDescribe(short_focal_img)
        M = self.matchKeypoints(kps_short, kps_long, featuresShort, featuresLong, ratio, reprojThresh)

        # 如果返回结果为空，没有匹配成功的特征点，退出算法
        if M is None:
            return None
        (matches, H, status) = M

        return H

    def transformation(self, image, H):
        result = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
        return result

    # 拼接函数
    def stitch(self, images, H):
        (long_focal_img, short_focal_img) = images

        long_focal_img = self.crop_image(long_focal_img, 0.75) - 100
        short_focal_img = self.crop_image(short_focal_img, -0.75)

        result = cv2.warpPerspective(short_focal_img, H,
                                     (short_focal_img.shape[1] + long_focal_img.shape[1], short_focal_img.shape[0]))
        # result *= 0.5

        # result[0:long_focal_img.shape[0], 0:long_focal_img.shape[1]] += long_focal_img
        result[0:long_focal_img.shape[0],
        int(long_focal_img.shape[1] * 0.25):long_focal_img.shape[1]] += long_focal_img[0:long_focal_img.shape[0],
                                                                        int(long_focal_img.shape[1] * 0.25):
                                                                        long_focal_img.shape[1]]

        return result[:, :-int(long_focal_img.shape[1] * 0.5)]

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


def transformation_by_norm(images):
    (long_focal_img, short_focal_img) = images
    stitcher = Stitcher()
    H_3_1, H_2_3 = get_norm_mtx()

    result = stitcher.stitch([long_focal_img, short_focal_img], H_3_1)
    return result
    # cv2.imshow('result', result)
    # cv2.waitKey(0)


def time_dropout_matching_check(camera_path_list, save_path, second=1):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    range_time = second * 300000000
    # 1669342684700000023
    stitcher = Stitcher()
    short_focal_img_norm = r'./test_data/norm_data/cm1.jpg'  # 5
    long_focal_img_norm = r'./test_data/norm_data/cm3.jpg'

    long_focal_img = cv2.imread(long_focal_img_norm)
    short_focal_img = cv2.imread(short_focal_img_norm)

    norm_H_3_1 = stitcher.get_M([long_focal_img, short_focal_img])

    camera1_base_path, camera2_base_path, camera3_base_path = camera_path_list
    camera1_file_list = os.listdir(camera1_base_path)
    camera2_file_list = os.listdir(camera2_base_path)
    camera3_file_list = os.listdir(camera3_base_path)
    camera1_file_list.sort()
    camera2_file_list.sort()
    camera3_file_list.sort()

    for index_1, cm1 in enumerate(camera1_file_list[3:]):
        Similarity_list = []
        img_list = []
        Time_path = os.path.join(save_path, str(cm1).split('.')[0])
        if not os.path.exists(Time_path):
            os.makedirs(Time_path)
        Time_cm1 = int(str(cm1).split('.')[0])

        cm1_file_path = os.path.join(camera1_base_path, cm1)
        short_focal_img = cv2.imread(cm1_file_path)

        for index_3, cm3 in enumerate(camera3_file_list):
            Time_cm3 = int(str(cm3).split('.')[0])
            if Time_cm3 < Time_cm1 + range_time and Time_cm3 > Time_cm1 - range_time:
                cm3_file_path = os.path.join(camera3_base_path, cm3)
                long_focal_img = cv2.imread(cm3_file_path)
                H_3_1 = stitcher.get_M([long_focal_img, short_focal_img])
                img = transformation_by_norm([long_focal_img, short_focal_img])
                Similarity = stitcher.mtx_similar(norm_H_3_1, H_3_1)

                fram_the = int((int(Time_cm1) - int(Time_cm3)) / 33333333)

                img_name = str(Time_cm1) + '_' + str(Time_cm3) + '_' + str(fram_the) + '_' + str(
                    Similarity) + '.png'
                print(img_name)
                end_save_path = os.path.join(Time_path, img_name)

                Similarity_list.append(Similarity)
                img_list.append({
                    'end_save_path': end_save_path,
                    'img': img,
                })

                # cv2.imwrite(end_save_path, img)
                # print(img_name)
        max_index = Similarity_list.index(max(Similarity_list))
        ret = img_list[max_index]
        end_save_path = ret['end_save_path']

        cv2.imwrite(end_save_path, ret['img'])


def top1(lst): return max(lst, default='列表为空', key=lambda v: lst.count(v))


def time_dropout_matching_check_fram(camera_path_list, save_path, second=1):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    range_time = second * 200000000
    # 1669342684700000023
    stitcher = Stitcher()
    short_focal_img_norm = r'./test_data/norm_data/cm1.jpg'  # 5
    long_focal_img_norm = r'./test_data/norm_data/cm3.jpg'

    long_focal_img = cv2.imread(long_focal_img_norm)
    short_focal_img = cv2.imread(short_focal_img_norm)

    norm_H_3_1 = stitcher.get_M([long_focal_img, short_focal_img])

    camera1_base_path, camera2_base_path, camera3_base_path = camera_path_list
    camera1_file_list = os.listdir(camera1_base_path)
    camera2_file_list = os.listdir(camera2_base_path)
    camera3_file_list = os.listdir(camera3_base_path)
    camera1_file_list.sort()
    camera2_file_list.sort()
    camera3_file_list.sort()
    big_ret = []
    step = 30*10
    for index_1, cm1 in enumerate(camera1_file_list[90003:]):
        if index_1 % step == 0:
            Similarity_list = []
            fram_the_list = []
            Time_path = os.path.join(save_path, str(cm1).split('.')[0])
            if not os.path.exists(Time_path):
                os.makedirs(Time_path)
            Time_cm1 = int(str(cm1).split('.')[0])

            cm1_file_path = os.path.join(camera1_base_path, cm1)
            short_focal_img = cv2.imread(cm1_file_path)

            for index_3, cm3 in enumerate(camera3_file_list[90000:]):
                Time_cm3 = int(str(cm3).split('.')[0])
                if Time_cm3 < Time_cm1 + range_time and Time_cm3 > Time_cm1 - range_time:
                    cm3_file_path = os.path.join(camera3_base_path, cm3)
                    long_focal_img = cv2.imread(cm3_file_path)
                    H_3_1 = stitcher.get_M([long_focal_img, short_focal_img])
                    Similarity = stitcher.mtx_similar(norm_H_3_1, H_3_1)
                    fram_the = int((int(Time_cm1) - int(Time_cm3)) / 33333330)
                    img = transformation_by_norm([long_focal_img, short_focal_img])

                    img_name = str(Time_cm1) + '_' + str(Time_cm3) + '_' + str(fram_the) + '_' + str(
                        Similarity) + '.png'
                    end_save_path = os.path.join(Time_path, img_name)

                    Similarity_list.append(Similarity)
                    fram_the_list.append(fram_the)

                    cv2.imwrite(end_save_path, img)
                    print(img_name)
            max_index = Similarity_list.index(max(Similarity_list))
            big_ret.append(fram_the_list[max_index])
    r = top1(big_ret)
    print(big_ret)
    print(r)


start = time.time()
time_dropout_matching_check_fram([r'/media/nas48/shucai/20230111/20230111_153435_output/record/camera1',
                                  r'/home/nailinliao/Desktop/DataDevelopment/SynchronousCheck/test_data/test_data/cm2',
                                  r'/media/nas48/shucai/20230111/20230111_153435_output/record/camera3'],
                                 r'/home/nailinliao/Desktop/20230111_step10second')

# time_dropout_matching_check_fram([r'/home/nailinliao/Desktop/DataDevelopment/SynchronousCheck/test_data/test_data/cm1',
#                                   r'/home/nailinliao/Desktop/DataDevelopment/SynchronousCheck/test_data/test_data/cm2',
#                                   r'/home/nailinliao/Desktop/DataDevelopment/SynchronousCheck/test_data/test_data/cm3'],
#                                  r'/home/nailinliao/Desktop/20230111')
print('time:', time.time() - start)
