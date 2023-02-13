'''
show video and Oscilloscope
'''
import os
import time

from Oscilloscope.V_0_1.Config import analysis_config_oscilloscope, config
from Oscilloscope.MP4_Tools import get_video_time
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


# class OscilloscopeLoader:
#     def __init__(self, oscilloscope_data_list, q_message: Queue, show_oscilloscope_secen_time=10):
#         self.oscilloscope_data_list = oscilloscope_data_list
#         self.q_message = q_message
#         self.step_time = show_oscilloscope_secen_time / 2
#         self.read_video_Process = Process(target=self.make_oscilloscope, args=())
#         self.read_video_Process.start()
#
#     def make_oscilloscope(self):
#         plt.ion()  # interactive mode on
#         fig, axs = plt.subplots(len(self.oscilloscope_data_list), constrained_layout=True)
#         for ax in axs.flat:
#             ax.label_outer()
#         line_list = []
#         for index, oscilloscope_data in enumerate(self.oscilloscope_data_list):
#             acx = axs[index]
#             property, _ = oscilloscope_data
#             acx.set_title(property)
#             line, = acx.plot([0, 1, 2, 3, 100], [0, 0, 0, 0, 100])
#             line_list.append(line)
#         while True:
#             if self.q_message.qsize() != 0:
#                 now_time = self.q_message.get()
#                 if now_time == 'q':
#                     break
#                 start_time = now_time - self.step_time
#                 end_time = now_time + self.step_time
#                 for index, oscilloscope_data in enumerate(self.oscilloscope_data_list):
#                     acx = axs[index]
#                     line = line_list[index]
#                     property, DataFrame = oscilloscope_data
#                     new_DataFrame = DataFrame[
#                         (DataFrame['Mesg_TimeStamp'] > start_time) & (
#                                 DataFrame['Mesg_TimeStamp'] < end_time)
#                         ]
#                     y = np.array(new_DataFrame[property])
#                     x = np.array(new_DataFrame['Mesg_TimeStamp'])
#                     line.set_data([x, y])
#                     acx.set_xlim(x[0], x[-1])
#                     acx.set_ylim(-min(y) * 0.5, max(y) * 1.5)
#                 plt.draw()
#                 plt.pause(0.00000001)
class OscilloscopeLoader:
    def __init__(self, oscilloscope_data_list, show_oscilloscope_secen_time=10):
        self.oscilloscope_data_list = oscilloscope_data_list
        self.step_time = show_oscilloscope_secen_time / 2
        plt.ion()  # interactive mode on
        self.fig, self.axs = plt.subplots(len(self.oscilloscope_data_list), constrained_layout=True)
        self.line_list = []
        for index, oscilloscope_data in enumerate(self.oscilloscope_data_list):
            acx = self.axs[index]
            property, _ = oscilloscope_data
            acx.set_title(property)
            line, = acx.plot([0, 1, 2, 3, 100], [0, 0, 0, 0, 100])
            self.line_list.append(line)

    def make_oscilloscope(self, now_time):
        start_time = now_time - self.step_time
        end_time = now_time + self.step_time
        for index, oscilloscope_data in enumerate(self.oscilloscope_data_list):
            acx = self.axs[index]
            line = self.line_list[index]
            property, DataFrame = oscilloscope_data
            new_DataFrame = DataFrame[
                (DataFrame['Mesg_TimeStamp'] > start_time) & (
                        DataFrame['Mesg_TimeStamp'] < end_time)
                ]
            y = np.array(new_DataFrame[property])
            x = np.array(new_DataFrame['Mesg_TimeStamp'])
            line.set_data([x, y])
            acx.set_xlim(x[0], x[-1])
            acx.set_ylim(-min(y) * 0.5, max(y) * 1.5)
        plt.draw()
        plt.pause(0.00000001)


def main(config):
    # 创建读取视频进程
    # 创建示波器进程，并等待时间戳输入
    video_path = r'/home/nailinliao/Desktop/camera1/1670812712066666690.mp4'
    oscilloscope_data_list = analysis_config_oscilloscope(config)
    time_secs, time_nans, time_floats = get_video_time(video_path)

    oscilloscopeLoader = OscilloscopeLoader(oscilloscope_data_list)
    for time_ in time_floats[:100]:
        strt = time.time()
        oscilloscopeLoader.make_oscilloscope(time_)
        print(1 / (time.time() - strt))


if __name__ == '__main__':
    main(config)
