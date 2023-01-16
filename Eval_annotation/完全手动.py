import os
from toolsFunction import matching_path, read_json_file, compute_iou_2D
import pandas as pd
import cv2


def property_judge(dict_gt: dict, dict_tar: dict):

    attributes = {
        'all_lights_off': 'all_lights_off',
        'brake_light_no': 'brake_light_no',
        'left_signal_visible': 'left_signal_visible',
        'right_signal_visible': 'right_signal_visible',
        "head_front": "head_front",
        "head_behind": "head_behind",
        "head_left": "head_left",
        "head_right": "head_right",
    }
    acc = 0
    sum = 1

    if dict_gt['type'] == dict_tar['type']:
        Hit_miss = False
        acc += 1
    else:
        Hit_miss = True
    data_gt = dict_gt.get('attributes')
    data_tar = dict_tar.get('attributes')

    gt=[]
    tar=[]


    for key in attributes:
        try:
            if data_gt.get(key) != None and data_tar.get(attributes[key]) != None:
                if data_gt.get(key) == data_tar.get(attributes[key]):
                    acc += 1
                sum += 1
        except:
            pass
    # print(Hit_miss, acc / sum)
    return Hit_miss, acc / sum


def compare_json(GT_json_file_path, tar_json_file_path, image_path):
    GT_json = read_json_file(GT_json_file_path)
    tar_json = read_json_file(tar_json_file_path)
    objects_GT = GT_json['objects']
    objects_Tar = tar_json['objects']
    recall = 0
    mIOU_2d = 0  # 需要除recall
    mIOU_3d = 0  # 需要除recall
    mHit_property = 0  # 需要除recall
    Class_Hit_miss_index = []
    Class_Hit_Rat = 1
    image_path = str(image_path).split('.')[0] + '.jpg'
    img = cv2.imread(image_path)
    recall_Rat = 0

    for index, tar in enumerate(objects_Tar):
        bbox_Tar = tar['bbox']

        rec_Tar = (
            float(bbox_Tar['ymin']), float(bbox_Tar['xmin']), float(bbox_Tar['ymax']), float(bbox_Tar['xmax']))

        pt1 = (int(rec_Tar[1]), int(rec_Tar[0]))
        pt2 = (int(rec_Tar[3]), int(rec_Tar[2]))
        cv2.rectangle(img, pt1, pt2, (255, 0, 0))

    for gt in objects_GT:
        bbox_GT = gt['bbox']
        # rec1: (y0, x0, y1, x1)
        rec_gt = (float(bbox_GT['ymin']), float(bbox_GT['xmin']), float(bbox_GT['ymax']), float(bbox_GT['xmax']))

        pt1 = (int(rec_gt[1]), int(rec_gt[0]))
        pt2 = (int(rec_gt[3]), int(rec_gt[2]))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255))

        for index, tar in enumerate(objects_Tar):
            bbox_Tar = tar['bbox']

            rec_Tar = (
                float(bbox_Tar['ymin']), float(bbox_Tar['xmin']), float(bbox_Tar['ymax']), float(bbox_Tar['xmax']))

            iou_2D = compute_iou_2D(rec_gt, rec_Tar)
            try:
                if iou_2D > 0.8:
                    recall += 1
                    Class_Hit_miss, Hit_mHit_property_rat = property_judge(gt, tar)
                    if not Class_Hit_miss:
                        Class_Hit_miss_index.append(index)
                    mHit_property += Hit_mHit_property_rat
                    mIOU_2d += iou_2D
            except:
                pass

    if recall != 0:
        mIOU_2d = mIOU_2d / recall
        mHit_property = mHit_property / recall
        Class_Hit_Rat = len(Class_Hit_miss_index) / recall
        recall_Rat = recall / (len(objects_GT) - 1)
        print('fileName:%s   ,mIOU_2d: %f   ,mHit_property_rat: %f ,recall_Rat:%f' % (
            GT_json['name'], mIOU_2d, mHit_property, recall_Rat))
        # cv2.imshow('image_' + str(len(objects_GT)), img)
        # cv2.waitKey(0)
    else:
        pass

    return mIOU_2d, mHit_property, Class_Hit_Rat, recall_Rat


def Evam_main(GT_path, Anotaion_path, images_base_path):
    careme_list = ['6mm', '12mm']
    DataFram = {
        'file_name': [],
        'mIOU_2d': [],
        'mHit_property_Rat': [],
        'Class_Hit_miss_Rat': [],
        'recall_Rat': [],
    }
    for careme in careme_list:
        GT_path_careme = os.path.join(GT_path, careme)
        Anotaion_path_careme = os.path.join(Anotaion_path, careme)

        image_path_careme = os.path.join(images_base_path, careme)

        hit_list = matching_path(GT_path_careme, Anotaion_path_careme)
        for file_name in hit_list:
            Gt_json_path = os.path.join(GT_path_careme, file_name)
            Anotaion_json_path = os.path.join(Anotaion_path_careme, file_name)
            image_path = os.path.join(image_path_careme, file_name)
            mIOU_2d, mHit_property, Class_Hit_miss_Rat, recall_Rat = compare_json(Gt_json_path,
                                                                                  Anotaion_json_path, image_path)
            file_name_carem = file_name + '_' + careme
            if mHit_property > 0.001 and recall_Rat > 0:
                DataFram['file_name'].append(file_name_carem)
                DataFram['mIOU_2d'].append(mIOU_2d)
                DataFram['mHit_property_Rat'].append(mHit_property)
                DataFram['Class_Hit_miss_Rat'].append(Class_Hit_miss_Rat)
                DataFram['recall_Rat'].append(recall_Rat)

    DataFram = pd.DataFrame(DataFram)
    return DataFram


def compare_json_HuoShan(GT_json_file_path, tar_json_file_path, image_path, location_Huoshan):
    GT_json = read_json_file(GT_json_file_path)
    tar_json = read_json_file(tar_json_file_path)

    if location_Huoshan == 1:
        objects_GT = GT_json
        objects_Tar = tar_json['objects']
    else:
        objects_GT = GT_json['objects']
        objects_Tar = tar_json

    recall = 0
    mIOU_2d = 0  # 需要除recall
    mHit_property = 0  # 需要除recall
    Class_Hit_miss_index = []
    Class_Hit_Rat = 1
    image_path = str(image_path).split('.')[0] + '.jpg'
    img = cv2.imread(image_path)
    recall_Rat = 0

    for gt in objects_GT:
        bbox_GT = gt['bbox']
        for index, tar in enumerate(objects_Tar):
            bbox_Tar = tar['bbox']

            if location_Huoshan == 1:
                rec_gt = (
                    float(bbox_GT['ymax']), float(bbox_GT['xmin']), float(bbox_GT['ymin']), float(bbox_GT['xmax']))

                rec_Tar = (
                    float(bbox_Tar['ymin']), float(bbox_Tar['xmin']), float(bbox_Tar['ymax']), float(bbox_Tar['xmax']))

            else:
                rec_gt = (
                    float(bbox_GT['ymin']), float(bbox_GT['xmin']), float(bbox_GT['ymax']), float(bbox_GT['xmax']))

                rec_Tar = (
                    float(bbox_Tar['ymax']), float(bbox_Tar['xmin']), float(bbox_Tar['ymin']), float(bbox_Tar['xmax']))

            iou_2D = compute_iou_2D(rec_gt, rec_Tar)
            if iou_2D > 0.8:
                try:
                    # print(iou_2D)
                    recall += 1
                    Class_Hit_miss, Hit_mHit_property_rat = property_judge(gt, tar)
                    if not Class_Hit_miss:
                        Class_Hit_miss_index.append(index)
                    mHit_property += Hit_mHit_property_rat
                    mIOU_2d += iou_2D
                except:
                    pass

    if recall != 0:
        mIOU_2d = mIOU_2d / recall
        mHit_property = mHit_property / recall
        Class_Hit_Rat = len(Class_Hit_miss_index) / recall
        recall_Rat = recall / (len(objects_GT) - 1)
        print('mIOU_2d: %f   ,mHit_property_rat: %f ,recall_Rat:%f' % (mIOU_2d, mHit_property, recall_Rat))
    else:
        pass
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    return mIOU_2d, mHit_property, Class_Hit_Rat, recall_Rat


def compare_json_HuoShan_A(GT_json_file_path, tar_json_file_path, image_path, location_Huoshan):
    GT_json = read_json_file(GT_json_file_path)
    tar_json = read_json_file(tar_json_file_path)

    objects_Tar = tar_json['objects']
    objects_GT = GT_json['objects']
    recall = 0
    mIOU_2d = 0  # 需要除recall
    mHit_property = 0  # 需要除recall
    Class_Hit_miss_index = []
    Class_Hit_Rat = 1
    image_path = str(image_path).split('.')[0] + '.jpg'
    img = cv2.imread(image_path)
    recall_Rat = 0

    for gt in objects_GT:
        bbox_GT = gt['bbox']
        for index, tar in enumerate(objects_Tar):
            bbox_Tar = tar['bbox']

            if location_Huoshan == 1:
                rec_gt = (
                    float(bbox_GT['ymax']), float(bbox_GT['xmin']), float(bbox_GT['ymin']), float(bbox_GT['xmax']))

                rec_Tar = (
                    float(bbox_Tar['ymin']), float(bbox_Tar['xmin']), float(bbox_Tar['ymax']), float(bbox_Tar['xmax']))

            else:
                rec_gt = (
                    float(bbox_GT['ymin']), float(bbox_GT['xmin']), float(bbox_GT['ymax']), float(bbox_GT['xmax']))

                rec_Tar = (
                    float(bbox_Tar['ymax']), float(bbox_Tar['xmin']), float(bbox_Tar['ymin']), float(bbox_Tar['xmax']))

            iou_2D = compute_iou_2D(rec_gt, rec_Tar)
            if iou_2D > 0.8:
                try:
                    # print(iou_2D)
                    recall += 1
                    Class_Hit_miss, Hit_mHit_property_rat = property_judge(gt, tar)
                    if not Class_Hit_miss:
                        Class_Hit_miss_index.append(index)
                    mHit_property += Hit_mHit_property_rat
                    mIOU_2d += iou_2D
                except:
                    pass

    if recall != 0:
        mIOU_2d = mIOU_2d / recall
        mHit_property = mHit_property / recall
        Class_Hit_Rat = len(Class_Hit_miss_index) / recall
        recall_Rat = recall / (len(objects_GT) - 1)
        print('mIOU_2d: %f   ,mHit_property_rat: %f ,recall_Rat:%f' % (mIOU_2d, mHit_property, recall_Rat))
    else:
        pass
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    return mIOU_2d, mHit_property, Class_Hit_Rat, recall_Rat


def Evam_main_Huoshan(GT_path, Anotaion_path, images_base_path, location_Huoshan):
    careme_list = ['6mm', '12mm']
    DataFram = {
        'file_name': [],
        'mIOU_2d': [],
        'mHit_property_Rat': [],
        'Class_Hit_miss_Rat': [],
        'recall_Rat': [],
    }
    for careme in careme_list:
        GT_path_careme = os.path.join(GT_path, careme)
        Anotaion_path_careme = os.path.join(Anotaion_path, careme)

        image_path_careme = os.path.join(images_base_path, careme)

        hit_list = matching_path(GT_path_careme, Anotaion_path_careme)
        for file_name in hit_list:
            Gt_json_path = os.path.join(GT_path_careme, file_name)
            Anotaion_json_path = os.path.join(Anotaion_path_careme, file_name)
            image_path = os.path.join(image_path_careme, file_name)
            mIOU_2d, mHit_property, Class_Hit_miss_Rat, recall_Rat = compare_json_HuoShan_A(Gt_json_path,
                                                                                            Anotaion_json_path,
                                                                                            image_path,
                                                                                            location_Huoshan)
            file_name_carem = file_name + '_' + careme
            if mHit_property > 0.001 and recall_Rat > 0:
                DataFram['file_name'].append(file_name_carem)
                DataFram['mIOU_2d'].append(mIOU_2d)
                DataFram['mHit_property_Rat'].append(mHit_property)
                DataFram['Class_Hit_miss_Rat'].append(Class_Hit_miss_Rat)
                DataFram['recall_Rat'].append(recall_Rat)

    DataFram = pd.DataFrame(DataFram)
    return DataFram


def Eval_function():
    images_base_path = r'C:\Users\NailinLiao\Desktop\camera_6_12mm_lidar_pcd_80'
    base_path = r'C:\Users\NailinLiao\Desktop\Anotation'
    DeepWay_path = os.path.join(base_path, 'DeepWay')
    Testing_path = os.path.join(base_path, 'Testing')
    Baidu_path = os.path.join(base_path, 'BaiDu_1')
    HuoSan_path = os.path.join(base_path, 'HuoShan')

    # DataFram = Evam_main(Baidu_path, DeepWay_path, images_base_path)
    # DataFram.to_csv("Baidu-DeepWay_B" + '.csv')

    # DataFram = Evam_main(DeepWay_path, Baidu_path, images_base_path)
    # DataFram.to_csv("DeepWay-Baidu_path_A" + '.csv')

    # DataFram = Evam_main(Testing_path, Baidu_path, images_base_path)
    # DataFram.to_csv("Testing-Baidu_path_A" + '.csv')

    DataFram = Evam_main_Huoshan(Baidu_path, HuoSan_path, images_base_path, 2)
    DataFram.to_csv("Baidu-Huoshan" + '.csv')
    # DataFram = Evam_main_Huoshan(Testing_path, HuoSan_path, images_base_path, 2)
    # DataFram.to_csv("Testing-Huoshan" + '.csv')
    # DataFram = Evam_main_Huoshan(DeepWay_path, HuoSan_path, images_base_path, 2)
    # DataFram.to_csv("DeepWay-Huoshan" + '.csv')
    #
    # DataFram = Evam_main_Huoshan(HuoSan_path, Baidu_path, images_base_path, 1)
    # DataFram.to_csv("Huoshan-Baidu" + '.csv')
    # DataFram = Evam_main(Testing_path, Baidu_path, images_base_path)
    # DataFram.to_csv("Testing-Baidu" + '.csv')
    # DataFram = Evam_main(DeepWay_path, Baidu_path, images_base_path)
    # DataFram.to_csv("DeepWay-Baidu" + '.csv')
    #
    # DataFram = Evam_main_Huoshan(HuoSan_path, Testing_path, images_base_path, 1)
    # DataFram.to_csv("Huoshan-Testing" + '.csv')
    # DataFram = Evam_main(DeepWay_path, Testing_path, images_base_path)
    # DataFram.to_csv("DeepWay-Testing" + '.csv')
    # DataFram = Evam_main(Baidu_path, Testing_path, images_base_path)
    # DataFram.to_csv("Baidu-Testing" + '.csv')
    #
    # DataFram = Evam_main_Huoshan(HuoSan_path, DeepWay_path, images_base_path, 1)
    # DataFram.to_csv("Huoshan-DeepWay_path" + '.csv')
    # DataFram = Evam_main(Testing_path, DeepWay_path, images_base_path)
    # DataFram.to_csv("Testing-DeepWay_path" + '.csv')
    # DataFram = Evam_main(Baidu_path, DeepWay_path, images_base_path)
    # DataFram.to_csv("Baidu-DeepWay_path" + '.csv')


def cout_Data_fram():
    path = r'./ret'
    file_list = os.listdir(path)
    ret_DataFram = {
        '对比情况': [],
        '2D标注框交并比': [],
        '属性命中率': [],
        '类别命中率': [],
        '召回率': [],
    }

    for file_name in file_list:
        file_path = os.path.join(path, file_name)
        DataFram = pd.read_csv(file_path)
        ret_DataFram['对比情况'].append(str(file_name).split('.')[0])
        ret_DataFram['2D标注框交并比'].append(DataFram['mIOU_2d'].mean())
        ret_DataFram['属性命中率'].append(DataFram['mHit_property_Rat'].mean())
        ret_DataFram['类别命中率'].append(DataFram['Class_Hit_miss_Rat'].mean())
        ret_DataFram['召回率'].append(DataFram['recall_Rat'].mean())

    print(ret_DataFram)
    pd.DataFrame(ret_DataFram).to_csv('all_data.csv')

if __name__ == '__main__':
    Eval_function()
