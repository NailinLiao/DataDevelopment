'''
show video and Oscilloscope
'''
import os
import time

from Config import analysis_config_oscilloscope, config
from MP4_Tools import get_video_time
from multiprocessing import Process, Queue
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

import numpy as np
from io import BytesIO


class OscilloscopeLoader:
    def __init__(self, oscilloscope_data_list, show_oscilloscope_secen_time=10):
        self.show_oscilloscope_secen_time = show_oscilloscope_secen_time
        self.oscilloscope_data_list = oscilloscope_data_list
        self.step_time = show_oscilloscope_secen_time / 2
        plt.ion()  # interactive mode on
        self.fig, self.axs = plt.subplots(len(self.oscilloscope_data_list), constrained_layout=True)
        self.line_list = []
        self.pix_list = []
        self.text = []
        for index, oscilloscope_data in enumerate(self.oscilloscope_data_list):
            acx = self.axs[index]
            acx.grid(True)

            property, _ = oscilloscope_data
            acx.set_title(property)
            line, = acx.plot([0, 1, 2, 3, 100], [0, 0, 0, 0, 100])
            pix, = acx.plot(0, 0, marker='o', markevery=10)

            self.line_list.append(line)
            self.pix_list.append(pix)

    def make_oscilloscope(self, now_time):
        start_time = now_time - self.step_time
        end_time = now_time + self.step_time
        for index, oscilloscope_data in enumerate(self.oscilloscope_data_list):
            acx = self.axs[index]
            line = self.line_list[index]
            pix = self.pix_list[index]
            property, DataFrame = oscilloscope_data
            new_DataFrame = DataFrame[
                (DataFrame['Mesg_TimeStamp'] > start_time) & (
                        DataFrame['Mesg_TimeStamp'] < end_time)
                ]
            y = np.array(new_DataFrame[property])
            x = np.array(new_DataFrame['Mesg_TimeStamp'])
            chout = 0
            for i in x:
                if i < now_time:
                    chout += 1

            cnet_x = now_time
            cent_y = y[chout]
            line.set_data([x, y])
            pix.set_data([cnet_x, cent_y])

            acx.set_xlim(x[0], x[-1])
            acx.set_xlabel(str(int(now_time)))
            acx.set_ylabel(str(cent_y))
            acx.set_ylim(-min(y) * 0.5, max(y) * 1.5)
            acx.set_xticks(np.arange(int(start_time), int(end_time), 2))

        plt.draw()
        self.fig.canvas.start_event_loop(0.001)
        # plt.pause(0.00000001)
        # plt.pause(0.1)


def main(config):
    # 创建读取视频进程
    # 创建示波器进程，并等待时间戳输入
    video_path = r'C:\Users\NailinLiao\Desktop/camera1/1670812712066666690.mp4'
    oscilloscope_data_list = analysis_config_oscilloscope(config)
    time_secs, time_nans, time_floats = get_video_time(video_path)

    oscilloscopeLoader = OscilloscopeLoader(oscilloscope_data_list)
    for time_ in time_floats[:100]:
        oscilloscopeLoader.make_oscilloscope(time_)


if __name__ == '__main__':
    main(config)
