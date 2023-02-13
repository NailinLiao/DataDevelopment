'''
show video and Oscilloscope
'''
import time
from Oscilloscope.V_0_1.Config import analysis_config_oscilloscope, config
from Oscilloscope.MP4_Tools import get_video_time
from multiprocessing import Process, Queue
from Oscilloscope_player import OscilloscopeLoader
import cv2
import matplotlib.pyplot as plt


def main(config):
    # 创建读取视频进程
    # 创建示波器进程，并等待时间戳输入
    show_oscilloscope_secen_time = config['Oscilloscope']['show_oscilloscope_secen_time']
    video_path = config['Video']['path']

    oscilloscope_data_list = analysis_config_oscilloscope(config)
    time_secs, time_nans, time_floats = get_video_time(video_path)

    time_secs, time_nans, time_floats = get_video_time(video_path)

    oscilloscopeLoader = OscilloscopeLoader(oscilloscope_data_list)

    cap = cv2.VideoCapture(video_path)

    for index, time_frame in enumerate(time_floats):
        strt = time.time()

        oscilloscopeLoader.make_oscilloscope(time_frame)
        statu, frame = cap.read()
        if statu:
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        print(1 / (time.time() - strt))

    time.sleep(10)


def test():
    pass


if __name__ == '__main__':
    main(config)
