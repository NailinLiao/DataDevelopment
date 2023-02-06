import time
import pandas as pd
import cv2
from multiprocessing import Process, Queue
from Oscilloscope.Config import config
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import numpy as np
from Oscilloscope.MP4_Tools import get_video_time


# https://www.jb51.net/article/206400.htm


# 设计为等待读取信号
# class OscilloscopeLoader:
#     def __init__(self, data_list: list, property: str, q_out: Queue, q_message: Queue, position=1, buffer=200,
#                  show_oscilloscope_len=100):
#         self.q_out = q_out
#         self.q_message = q_message
#         self.property = property
#         self.data_list = data_list
#         self.buffer = buffer
#         self.show_oscilloscope_len = show_oscilloscope_len
#         self.read_video_Process = Process(target=self.make_oscilloscope, args=(position,))
#         self.read_video_Process.start()
#
#     def show_oscilloscope(self, index: int, step=50):
#         head = index - step
#         end = index + step
#         show_oscilloscope_list = self.data_list[head:end]
#
#         # time = np.arange(0, len(show_oscilloscope_list)) * (1.0 / sr)
#         time = np.arange(head, end)
#         y = np.mean(show_oscilloscope_list[step:step + 1])
#         x = time[step]
#         text = 'frame index:' + str(index) + '___value:' + str(y)
#         plt.text(x, y, text, ha='left', wrap=True)
#         plt.scatter(y=show_oscilloscope_list[step:step + 1], x=time[step:step + 1], s=10, )
#         plt.plot(time, show_oscilloscope_list)
#         plt.title(self.property, loc='center')
#         buffer = BytesIO()
#         plt.savefig(buffer, format='png')
#         buffer.seek(0)
#         data_img = Image.open(buffer)
#         data_img = np.array(data_img)
#         plt.clf()
#         return data_img
#
#     def make_oscilloscope(self, position):
#         step = int(self.show_oscilloscope_len / 2)
#         if position < step:
#             index = step
#         elif position > len(self.data_list) - step:
#             index = len(self.data_list) - step
#
#         data_len = len(self.data_list)
#         while index + step < data_len:
#             if self.q_out.qsize() < self.buffer:
#                 self.q_out.put(self.show_oscilloscope(index, step))
#             if self.q_message.qsize() != 0:
#                 index = self.q_message.get()
#                 print('------', index)
#                 if index < step:
#                     index = step
#                 elif index > len(self.data_list) - step:
#                     index = len(self.data_list) - step
#                 # 清理管道
#                 while self.q_out.qsize() > 0:
#                     print('清理管道', self.q_out.qsize())
#                     _ = self.q_out.get()
#             index += 1

class OscilloscopeLoader:
    def __init__(self, DataFrame: pd.DataFrame, property: str, time_list: list, q_out: Queue, q_message: Queue,
                 buffer=200,
                 show_oscilloscope_time=5):
        self.DataFrame = DataFrame

        self.q_out = q_out
        self.q_message = q_message
        self.property = property
        self.buffer = buffer
        self.show_oscilloscope_time = show_oscilloscope_time
        self.time_list = time_list
        self.time_list.reverse()
        self.step_time = int(self.show_oscilloscope_time / 2)

        self.read_video_Process = Process(target=self.make_oscilloscope, args=())
        self.read_video_Process.start()

    def make_oscilloscope(self):
        while len(self.time_list) != 0:
            if self.q_message.qsize() != 0:
                self.time_list = self.q_message.get()
                self.time_list.reverse()
                while self.q_out.qsize() > 0:
                    _ = self.q_out.get()
            now_time = self.time_list.pop()
            start_time = now_time - self.step_time
            end_time = now_time + self.step_time
            new_DataFrame = self.DataFrame[
                (self.DataFrame['Mesg_TimeStamp'] > start_time) & (
                        self.DataFrame['Mesg_TimeStamp'] < end_time)
                ]
            if len(new_DataFrame) == 0:
                y = [0, 0, 0, 0, 0, 0, 0]
                x = [0, 0, 0, 0, 0, 0, 0]
            else:
                y = new_DataFrame[self.property]
                x = new_DataFrame['Mesg_TimeStamp']
            # plt.scatter(y=y, x=x)
            plt.plot(x, y)
            plt.title(self.property, loc='center')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            data_img = Image.open(buffer)
            data_img = np.array(data_img)
            plt.clf()
            self.q_out.put(data_img)
            # cv2.imshow('m', data_img)
            # cv2.waitKey(1)
            # return data_img


def test():
    ins_data = r'/home/nailinliao/Desktop/radar1/1670812712096032405_EBC2_EBS.csv'
    video_path = config['Video']['path']
    Radar_path = config['Oscilloscope']['Radar_path']
    show_oscilloscope_len = config['Oscilloscope']['show_oscilloscope_secen_time']
    videoCapture = cv2.VideoCapture(video_path)
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    Video_HZ = config['Video']['HZ']
    # 创建读取视频进程
    # 创建示波器进程，并等待时间戳输入

    time_secs, time_nans, time_floats = get_video_time(video_path)
    DataFrame = pd.read_csv(ins_data)
    property = 'Front_Axle_Speed'

    q_video = Queue()  # 创建队列
    q_message = Queue()  # 创建队列

    oscilloscopeLoader_loader = OscilloscopeLoader(DataFrame, property, time_floats, q_video, q_message)
    time.sleep(10)


test()
