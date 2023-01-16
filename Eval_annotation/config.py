targ_type = {
    'Car': '小汽车',
    'Van': '面包车',
    'light_truck': '轻卡',
    'heavy_truck': '重卡',
    'tow_truck': '救援拖车',
    'Truck': '卡车',
    'trailer': '挂车',
    'engineering_truck': '工程车',
    'bus': '大巴车',
    'electronic_car': '四轮小车',
    'fire_engine': '消防车',
    'motorcycle': '摩托车',
    'tricycle': '三轮车',
    'scooter': '踏板车',
    'bicycle': '自行车',
    'traffic_cone': '锥形桶',
    'sign': '指示牌',
    'pedestrian': '行人',
    'pram': '婴儿车',
    'wheelchair': '轮椅',
    'pull_push_objects': '可推拉物体',
    'small_animals': '小型动物',
    'big_animals': '大型动物',
    'debris': '碎片',
    'dontcare': {
        # “忽略” 子类
        'crowd_dontcare': '人群忽略',
        'vehicle_dontcare': '车群忽略',
        'bikes_group_dontcare': '自行车群忽略',
        'other_dontcare': '其他忽略',
    },
}

type_list = ['Car', 'Van', 'light_truck', 'heavy_truck', 'tow_truck', 'Truck', 'trailer', 'engineering_truck', 'bus',
             'electronic_car', 'fire_engine', 'motorcycle', 'tricycle', 'scooter', 'bicycle', 'traffic_cone', 'sign',
             'pedestrian', 'pram', 'wheelchair', 'pull_push_objects', 'small_animals', 'big_animals', 'debris',
             'dontcare']
car_lights = ['Car', 'Van', 'light_truck', 'heavy_truck', 'tow_truck', 'Truck', 'trailer',
              'engineering_truck', 'bus',
              'electronic_car', 'fire_engine']
with_person = ['motorcycle', 'bicycle', 'scooter', 'pram', 'wheelchair']
pedestrian_pose = ['pedestrian']
cleaning_trolley = ['light_truck']
police = ['light_truck', 'Car', 'motorcycle']
emergency = ['Van']
head = ['Car', 'Van', 'light_truck', 'heavy_truck', 'tow_truck', 'Truck', 'trailer', 'engineering_truck',
        'bus',
        'electronic_car', 'fire_engine']

targ_property = {
    'type': type_list,
    'bbox': type_list,
    'dimensions': type_list,
    'location': type_list,
    'rotation_y': type_list,
    'occluded': type_list,
    'truncation': type_list,
    'with_person': with_person,
    'pedestrian_pose': pedestrian_pose,
    'all_lights_off': car_lights,
    'brake_lights_on': car_lights,
    'left_signal_visible': car_lights,
    'right_signal_visible': car_lights,
    'double_flash_no': car_lights,
    'cleaning_trolley': cleaning_trolley,
    'police': police,
    'emergency': emergency,
    'head_front': head,
    'head_behind': head,
    'head_left': head,
    'head_right': head,
}
2
type_property = {
    'Car': {'type': 'Car', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
            'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X', 'left_signal_visible': 'X',
            'right_signal_visible': 'X', 'double_flash_no': 'X', 'police': 'X', 'head_front': 'X', 'head_behind': 'X',
            'head_left': 'X', 'head_right': 'X'},
    'Van': {'type': 'Van', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
            'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X', 'left_signal_visible': 'X',
            'right_signal_visible': 'X', 'double_flash_no': 'X', 'emergency': 'X', 'head_front': 'X',
            'head_behind': 'X', 'head_left': 'X', 'head_right': 'X'},
    'light_truck': {'type': 'light_truck', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                    'occluded': 'X', 'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X',
                    'left_signal_visible': 'X', 'right_signal_visible': 'X', 'double_flash_no': 'X',
                    'cleaning_trolley': 'X', 'police': 'X', 'head_front': 'X', 'head_behind': 'X', 'head_left': 'X',
                    'head_right': 'X'},
    'heavy_truck': {'type': 'heavy_truck', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                    'occluded': 'X', 'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X',
                    'left_signal_visible': 'X', 'right_signal_visible': 'X', 'double_flash_no': 'X', 'head_front': 'X',
                    'head_behind': 'X', 'head_left': 'X', 'head_right': 'X'},
    'tow_truck': {'type': 'tow_truck', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                  'occluded': 'X', 'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X',
                  'left_signal_visible': 'X', 'right_signal_visible': 'X', 'double_flash_no': 'X', 'head_front': 'X',
                  'head_behind': 'X', 'head_left': 'X', 'head_right': 'X'},
    'Truck': {'type': 'Truck', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
              'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X', 'left_signal_visible': 'X',
              'right_signal_visible': 'X', 'double_flash_no': 'X', 'head_front': 'X', 'head_behind': 'X',
              'head_left': 'X', 'head_right': 'X'},
    'trailer': {'type': 'trailer', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
                'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X', 'left_signal_visible': 'X',
                'right_signal_visible': 'X', 'double_flash_no': 'X', 'head_front': 'X', 'head_behind': 'X',
                'head_left': 'X', 'head_right': 'X'},
    'engineering_truck': {'type': 'engineering_truck', 'bbox': 'X', 'dimensions': 'X', 'location': 'X',
                          'rotation_y': 'X', 'occluded': 'X', 'truncation': 'X', 'all_lights_off': 'X',
                          'brake_lights_on': 'X', 'left_signal_visible': 'X', 'right_signal_visible': 'X',
                          'double_flash_no': 'X', 'head_front': 'X', 'head_behind': 'X', 'head_left': 'X',
                          'head_right': 'X'},
    'bus': {'type': 'bus', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
            'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X', 'left_signal_visible': 'X',
            'right_signal_visible': 'X', 'double_flash_no': 'X', 'head_front': 'X', 'head_behind': 'X',
            'head_left': 'X', 'head_right': 'X'},
    'electronic_car': {'type': 'electronic_car', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                       'occluded': 'X', 'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X',
                       'left_signal_visible': 'X', 'right_signal_visible': 'X', 'double_flash_no': 'X',
                       'head_front': 'X', 'head_behind': 'X', 'head_left': 'X', 'head_right': 'X'},
    'fire_engine': {'type': 'fire_engine', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                    'occluded': 'X', 'truncation': 'X', 'all_lights_off': 'X', 'brake_lights_on': 'X',
                    'left_signal_visible': 'X', 'right_signal_visible': 'X', 'double_flash_no': 'X', 'head_front': 'X',
                    'head_behind': 'X', 'head_left': 'X', 'head_right': 'X'},
    'motorcycle': {'type': 'motorcycle', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                   'occluded': 'X', 'truncation': 'X', 'with_person': 'X', 'police': 'X'},
    'tricycle': {'type': 'tricycle', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                 'occluded': 'X', 'truncation': 'X'},
    'scooter': {'type': 'scooter', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
                'truncation': 'X', 'with_person': 'X'},
    'bicycle': {'type': 'bicycle', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
                'truncation': 'X', 'with_person': 'X'},
    'traffic_cone': {'type': 'traffic_cone', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                     'occluded': 'X', 'truncation': 'X'},
    'sign': {'type': 'sign', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
             'truncation': 'X'},
    'pedestrian': {'type': 'pedestrian', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                   'occluded': 'X', 'truncation': 'X', 'pedestrian_pose': 'X'},
    'pram': {'type': 'pram', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
             'truncation': 'X', 'with_person': 'X'},
    'wheelchair': {'type': 'wheelchair', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                   'occluded': 'X', 'truncation': 'X', 'with_person': 'X'},
    'pull_push_objects': {'type': 'pull_push_objects', 'bbox': 'X', 'dimensions': 'X', 'location': 'X',
                          'rotation_y': 'X', 'occluded': 'X', 'truncation': 'X'},
    'small_animals': {'type': 'small_animals', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                      'occluded': 'X', 'truncation': 'X'},
    'big_animals': {'type': 'big_animals', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                    'occluded': 'X', 'truncation': 'X'},
    'debris': {'type': 'debris', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X', 'occluded': 'X',
               'truncation': 'X'},
    'dontcare': {'type': 'dontcare', 'bbox': 'X', 'dimensions': 'X', 'location': 'X', 'rotation_y': 'X',
                 'occluded': 'X', 'truncation': 'X'}}


def get_type_property():
    type_fort_dict = {}

    for tar_type in type_list:
        type_dict = {}
        for key in targ_property:
            if tar_type in targ_property[key]:
                if key == 'type':
                    type_dict[key] = tar_type
                else:
                    type_dict[key] = 'X'
        type_fort_dict[tar_type] = type_dict
    print(type_fort_dict)


if __name__ == '__main__':
    get_type_property()
