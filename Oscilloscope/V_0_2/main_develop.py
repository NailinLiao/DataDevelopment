'''
show video and Oscilloscope
'''
from V_0_2.Config import analysis_config_oscilloscope, config
from MP4_Tools import get_video_time
from multiprocessing import Process, Queue
from Oscilloscope_player import OscilloscopeLoader
import cv2
# from mark_label import Marker


def main(config):
    show_oscilloscope_secen_time = config['Oscilloscope']['show_oscilloscope_secen_time']
    video_path = config['Video']['path']
    oscilloscope_data_list = analysis_config_oscilloscope(config)
    time_secs, time_nans, time_floats = get_video_time(video_path)
    oscilloscopeLoader = OscilloscopeLoader(oscilloscope_data_list, show_oscilloscope_secen_time)
    SaveJsonPath = config['SaveJsonPath']
    # maker = Marker(video_path, SaveJsonPath)
    print('----')
    cap = cv2.VideoCapture(video_path)
    Run = True
    index = 0
    while index < len(time_floats):
        time_frame = time_floats[index]
        if index % 5 == 0:
            oscilloscopeLoader.make_oscilloscope(time_frame)
        if Run:
            statu, frame = cap.read()

            index += 1
        else:
            # 启动标注页面
            if key == 81:
                index -= 5
                oscilloscopeLoader.make_oscilloscope(time_frame)
                cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                _, _ = cap.read()
                statu, frame = cap.read()
                cv2.imshow('frame', frame)
            if key == 83:
                index += 5
                oscilloscopeLoader.make_oscilloscope(time_frame)
                cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                _, _ = cap.read()
                statu, frame = cap.read()
                cv2.imshow('frame', frame)
        cv2.imshow('frame', frame)

        key = cv2.waitKey(1)

        if key == 32:
            Run = bool(1 - Run)
    # maker.kill()


if __name__ == '__main__':
    main(config)
