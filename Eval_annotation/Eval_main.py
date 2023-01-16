import os
from toolsFunction import compare_json, matching_path
import pandas as pd


def Evam_main(GT_path, Anotaion_path):
    careme_list = ['6mm', '12mm']
    DataFram = {
        'file_name': [],
        'mIOU_2d': [],
        'mIOU_3d': [],
        'mHit_property': [],
        'recall_rat': [],
        'Class_Hit_miss_index': [],
    }
    for careme in careme_list:
        GT_path_careme = os.path.join(GT_path, careme)
        Anotaion_path_careme = os.path.join(Anotaion_path, careme)
        hit_list = matching_path(GT_path_careme, Anotaion_path_careme)
        for file_name in hit_list:
            Gt_json_path = os.path.join(GT_path_careme, file_name)
            Anotaion_json_path = os.path.join(Anotaion_path_careme, file_name)
            mIOU_2d, mIOU_3d, mHit_property, recall_rat, Class_Hit_miss_index = compare_json(Gt_json_path,
                                                                                             Anotaion_json_path)
            file_name_carem = file_name + '_' + careme
            DataFram['file_name'].append(file_name_carem)
            DataFram['mIOU_2d'].append(mIOU_2d)
            DataFram['mIOU_3d'].append(mIOU_3d)
            DataFram['mHit_property'].append(mHit_property)
            DataFram['recall_rat'].append(recall_rat)
            DataFram['Class_Hit_miss_index'].append(Class_Hit_miss_index)

    DataFram = pd.DataFrame(DataFram)
    return DataFram


def Eval_function():
    base_path = r'C:\Users\NailinLiao\Desktop\Anotation'
    DeepWay_path = os.path.join(base_path, 'DeepWay')
    Testing_path = os.path.join(base_path, 'Testing')
    Baidu_path = os.path.join(base_path, 'Baidu')

    DataFram = Evam_main(DeepWay_path, Testing_path)
    DataFram.to_csv("DeepWay-Testing" + '.csv')

    # DataFram = Evam_main(DeepWay_path, Testing_path)
    # DataFram.to_csv("DeepWay-Baidu" + '.csv')


if __name__ == '__main__':
    Eval_function()
