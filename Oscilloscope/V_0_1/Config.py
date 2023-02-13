import os
import pandas as pd

config = {
    'Video': {
        'path': r'/home/nailinliao/Desktop/camera1/1670812712066666690.mp4',
    },
    'Oscilloscope':
        {
            'Radar_path': r'/home/nailinliao/Desktop/radar1',
            'show_oscilloscope_secen_time': 10,
            'select': {
                'EBC2_EBS': ['Front_Axle_Speed', 'Front_Axle_Speed'],
                # HZ：1，30，60,140
            }
        }
}


def analysis_config_oscilloscope(config):
    '''
    解析配置文件中要求展示的波形数据
    '''
    Radar_path = config['Oscilloscope']['Radar_path']
    oscilloscope = config['Oscilloscope']['select']

    oscilloscope_data_list = []
    csv_file_list = os.listdir(Radar_path)
    for key in oscilloscope:
        for csv_file in csv_file_list:
            if key in csv_file:
                csv_path = os.path.join(Radar_path, csv_file)
                DataFrame = pd.read_csv(csv_path)
                property_list = oscilloscope[key]
                for property in property_list:
                    oscilloscope_data_list.append([property, DataFrame])
    return oscilloscope_data_list
