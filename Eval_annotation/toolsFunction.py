import json
import os


def read_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as fw:
        json_data = json.load(fw)
        return json_data


def get_file_list(base_file_path):
    file_name_list = os.listdir(base_file_path)
    return [(os.path.join(base_file_path, file_name)) for file_name in file_name_list]


def compute_iou_2D(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect)) * 1.0


# def compute_iou_3D(box1, box2):
#     '''
#         box [x1,y1,z1,x2,y2,z2]   分别是两对角定点的坐标
#     '''
#     area1 = (box1[3] - box1[0]) * (box1[4] - box1[1]) * (box1[5] - box1[2])
#     area2 = (box2[3] - box2[0]) * (box2[4] - box2[1]) * (box2[5] - box2[2])
#     area_sum = area1 + area2
#
#     # 计算重叠部分 设重叠box坐标为 [x1,y1,z1,x2,y2,z2]
#     x1 = max(box1[0], box2[0])
#     y1 = max(box1[1], box2[1])
#     z1 = max(box1[2], box2[2])
#     x2 = min(box1[3], box2[3])
#     y2 = min(box1[4], box2[4])
#     z2 = min(box1[5], box2[5])
#
#     inter_area = (x2 - x1) * (y2 - y1) * (z2 - z1)
#
#     return inter_area / (area_sum - inter_area)

def compute_iou_3D(box1, box2):
    '''
    3D IoU计算
    box表示形式：[x1,y1,z1,x2,y2,z2] 分别是两对角点的坐标
    '''
    in_w = min(box1[3], box2[3]) - max(box1[0], box2[0])
    in_l = min(box1[4], box2[4]) - max(box1[1], box2[1])
    in_h = min(box1[5], box2[5]) - max(box1[2], box2[2])

    inter = 0 if in_w < 0 or in_l < 0 or in_h < 0 else in_w * in_l * in_h
    union = (box1[3] - box1[0]) * (box1[4] - box1[1]) * (box1[5] - box1[2]) + (box2[3] - box2[0]) * (
            box2[4] - box2[1]) * (box2[5] - box2[2]) - inter
    iou = inter / union
    return iou


# def property_judge(dict_gt: dict, dict_tar: dict):
#     sum = 0
#     attribute_acc = 0
#     Hit_miss = False
#     if dict_gt['type'] == dict_tar['type']:
#         attribute_acc += 1
#         sum += 1
#     else:
#         Hit_miss = True
#     attributes_gt = dict_gt.get('attributes')
#     attributes_tar = dict_tar.get('attributes')
#     for key in attributes_gt:
#         if attributes_gt.get(key) == attributes_tar.get(key):
#             attribute_acc += 1
#         sum += 1
#     if sum != 0:
#         return Hit_miss, attribute_acc / sum
#
#     else:
#         return Hit_miss, 1

def property_judge(dict_gt: dict, dict_tar: dict):
    acc = 0
    sum = 1
    if dict_gt['type'] == dict_tar['type']:
        Hit_miss = False
        acc += 1
    else:
        Hit_miss = True

    data_gt = dict_gt.get('attributes')
    data_tar = dict_tar.get('attributes')
    try:
        for key in data_gt:
            data_key_gt = data_gt.get(key)
            data_key_tar = data_tar.get(key)
            if data_key_tar != None:
                if data_key_gt == data_key_tar:
                    acc += 1
                sum += 1
    except:
        pass

    return Hit_miss, acc / sum


def get_3d_2d_box(json_data):
    # 遗留 bug 需要确认 空间坐标系。
    # dimensions_gt = json_data['dimensions']
    # location_gt = json_data['location']
    dimensions_gt = json_data.get('dimensions')
    location_gt = json_data.get('location')
    if dimensions_gt != None and location_gt != None:
        '''
            box [x1,y1,z1,x2,y2,z2]   分别是两对角定点的坐标
        '''
        box_3d_x = abs(float(location_gt['x']))
        box_3d_y = abs(float(location_gt['y']))
        box_3d_z = abs(float(location_gt['z']))
        w = abs(float(dimensions_gt['w']))
        h = abs(float(dimensions_gt['h']))
        l = abs(float(dimensions_gt['l']))

        box_3d = [box_3d_x, box_3d_y, box_3d_z,
                  box_3d_x + w,
                  box_3d_y + h,
                  box_3d_z + l]
        return box_3d
    else:
        return [-1, -1, -1, -1, -1, -1]


def compare_json(GT_json_file_path, tar_json_file_path):
    GT_json = read_json_file(GT_json_file_path)
    tar_json = read_json_file(tar_json_file_path)
    objects_GT = GT_json['objects']
    objects_Tar = tar_json['objects']
    recall = 0
    mIOU_2d = 0  # 需要除recall
    mIOU_3d = 0  # 需要除recall
    mHit_property = 0  # 需要除recall
    Class_Hit_miss_index = []
    recall_rat = 0
    for gt in objects_GT:
        bbox_GT = gt['bbox']
        # rec1: (y0, x0, y1, x1)
        rec_gt = (float(bbox_GT['ymin']), float(bbox_GT['xmin']), float(bbox_GT['ymax']), float(bbox_GT['xmax']))
        for index, tar in enumerate(objects_Tar):
            bbox_Tar = tar['bbox']
            rec_Tar = (
                float(bbox_Tar['ymin']), float(bbox_Tar['xmin']), float(bbox_Tar['ymax']), float(bbox_Tar['xmax']))

            iou_2D = compute_iou_2D(rec_gt, rec_Tar)
            if iou_2D > 0.8:
                recall += 1
                bbox_3d_gt = get_3d_2d_box(gt)

                bbox_3d_tar = get_3d_2d_box(tar)
                iou_3D = compute_iou_3D(bbox_3d_gt, bbox_3d_tar)
                Class_Hit_miss, Hit_mHit_property_rat = property_judge(gt, tar)
                if Class_Hit_miss:
                    Class_Hit_miss_index.append(index)
                mHit_property += Hit_mHit_property_rat
                mIOU_2d += iou_2D
                mIOU_3d += iou_3D
    if recall != 0:
        mIOU_2d = mIOU_2d / recall
        mIOU_3d = mIOU_3d / recall
        mHit_property = mHit_property / recall
        recall_rat = len(objects_Tar) / len(objects_GT)
        print('fileName:%s   ,mIOU_2d: %f  ,mIOU_3d: %f  ,mHit_property_rat: %f  ,recall_rat: %f' % (
            GT_json['name'], mIOU_2d, mIOU_3d, mHit_property, recall_rat))
    return mIOU_2d, mIOU_3d, mHit_property, recall_rat, Class_Hit_miss_index


# def compare_json(GT_json_file_path, tar_json_file_path):
#     GT_json = read_json_file(GT_json_file_path)
#     tar_json = read_json_file(tar_json_file_path)
#     objects_GT = GT_json['objects']
#     objects_Tar = tar_json['objects']
#     recall = 0
#     mIOU_2d = 0  # 需要除recall
#     mIOU_3d = 0  # 需要除recall
#     mHit_property = 0  # 需要除recall
#     Class_Hit_miss_index = []
#     for gt in objects_GT:
#         bbox_GT = gt['bbox']
#         # rec1: (y0, x0, y1, x1)
#         rec_gt = (float(bbox_GT['ymin']), float(bbox_GT['xmin']), float(bbox_GT['ymax']), float(bbox_GT['xmax']))
#         for index, tar in enumerate(objects_Tar):
#             bbox_Tar = tar['bbox']
#             rec_Tar = (
#                 float(bbox_Tar['ymin']), float(bbox_Tar['xmin']), float(bbox_Tar['ymax']), float(bbox_Tar['xmax']))
#
#             iou_2D = compute_iou_2D(rec_gt, rec_Tar)
#
#             if iou_2D > 0.8:
#                 recall += 1
#                 bbox_3d_gt = get_3d_2d_box(gt)
#                 bbox_3d_tar = get_3d_2d_box(tar)
#                 iou_3D = compute_iou_3D(bbox_3d_gt, bbox_3d_tar)
#                 mIOU_2d += iou_2D
#                 mIOU_3d += iou_3D
#
#                 Class_Hit_miss, Hit_mHit_property_rat = property_judge(gt, tar)
#                 if Class_Hit_miss:
#                     Class_Hit_miss_index.append(index)
#                 mHit_property += Hit_mHit_property_rat
#     if recall != 0:
#         mHit_property = mHit_property / recall
#         mIOU_3d = mIOU_3d / recall
#         mIOU_2d = mIOU_2d / recall
#         recall_rat = recall / len(objects_Tar)
#         print('fileName:%s   ,mIOU_2d: %f  ,mIOU_3d: %f  ,mHit_property_rat: %f  ,recall_rat: %f' % (
#             GT_json['name'], mIOU_2d, mIOU_3d, mHit_property, recall_rat))
#         return mIOU_2d, mIOU_3d, mHit_property, recall_rat, Class_Hit_miss_index
#     else:
#         return mIOU_2d, mIOU_3d, mHit_property, 0, Class_Hit_miss_index


def matching_path(GT_path, Anotaion_path):
    hit = []

    file_list_GT = os.listdir(GT_path)
    file_list_Anotaion = os.listdir(Anotaion_path)
    for file_name in file_list_GT:
        if file_name in file_list_Anotaion:
            hit.append(file_name)
    return hit


def demo_one():
    base_file_path = r'C:\Users\NailinLiao\Desktop\lidar_pcd\camera_6mm\0006.json'
    base_file_path2 = r'C:\Users\NailinLiao\Desktop\lidar_pcd\camera_6mm\0006.json'

    compare_json(base_file_path, base_file_path2)


if __name__ == '__main__':
    demo_one()
