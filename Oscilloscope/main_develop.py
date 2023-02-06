'''
show video and Oscilloscope
'''
import time
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import pandas as pd
from multiprocessing import Process, Queue
from Config import config
from Loader.Oscilloscope_player import *
from Loader.Video_player import *
from MP4_Tools import get_video_time


def analysis_config_oscilloscope(config):
    '''
    解析配置文件中要求展示的波形数据
    '''
    Radar_path = config['Radar_path']
    oscilloscope = config['oscilloscope']

    oscilloscope_data_list = []

    csv_file_list = os.listdir(Radar_path)
    for key in oscilloscope:
        for csv_file in csv_file_list:
            if key in csv_file:
                csv_path = os.path.join(Radar_path, csv_file)
                DataFrame = pd.read_csv(csv_path)
                property_list = oscilloscope[key]
                for property in property_list:
                    oscilloscope_data_list.append([property, DataFrame[property]])
    return oscilloscope_data_list


# def main(config):
#     video_path = config['Video_path']
#     Radar_path = config['Radar_path']
#     show_oscilloscope_len = config['show_oscilloscope_len']
#     oscilloscope = config['oscilloscope']
#
#     # 播放
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     wait = int(1 / fps * 700)
#     csv_file_list = os.listdir(Radar_path)
#
#     q_oscilloscopeLoader_list = []
#     q_oscilloscope_message_list = []
#
#     for key in oscilloscope:
#         for csv_file in csv_file_list:
#             if key in csv_file:
#                 csv_path = os.path.join(Radar_path, csv_file)
#                 DataFrame = pd.read_csv(csv_path)
#                 for property in oscilloscope[key]:
#                     property_list = DataFrame[property]
#                     q_oscilloscopeLoader = Queue()
#                     q_message = Queue()
#                     q_oscilloscopeLoader_list.append(q_oscilloscopeLoader)
#                     q_oscilloscope_message_list.append(q_message)
#                     oscilloscopeLoader_loader = OscilloscopeLoader(property_list, key, q_oscilloscopeLoader, q_message,
#                                                                    show_oscilloscope_len=show_oscilloscope_len)


def main(config):
    video_path = config['Video']['path']
    Radar_path = config['Oscilloscope']['Radar_path']
    show_oscilloscope_len = config['Oscilloscope']['show_oscilloscope_secen_time']
    videoCapture = cv2.VideoCapture(video_path)
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    Video_HZ = config['Video']['HZ']
    # 创建读取视频进程
    # 创建示波器进程，并等待时间戳输入

    time_secs, time_nans, time_floats = get_video_time(video_path)
    for inde, time_float in time_floats:
        pass


if __name__ == '__main__':
    main(config)
