import time

import cv2
from multiprocessing import Process, Queue
from Oscilloscope.Config import config


class VideoLoader:
    def __init__(self, video_path, q_out: Queue, q_message: Queue, buffer=200, position=1):
        self.video_path = video_path
        self.q_out = q_out
        self.q_message = q_message
        self.buffer = buffer
        self.read_video_Process = Process(target=self.read_frame, args=(position,))
        self.read_video_Process.start()

    def initialization_position(self, position):
        self.cap = cv2.VideoCapture(self.video_path)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        _, _ = self.cap.read()

    def read_frame(self, position=1):
        self.initialization_position(position)
        while True:
            if self.q_message.qsize() != 0:
                position = self.q_message.get()
                self.initialization_position(position)
                # self.clean_queue()
                while self.q_out.qsize() > 0:
                    _ = self.q_out.get()
                    # time.sleep(1)
            if self.q_out.qsize() < self.buffer:
                statu, frame = self.cap.read()
                if statu:
                    self.q_out.put(frame)
                else:
                    return


def test():
    video_path = config['Video_path']
    q_video = Queue()  # 创建队列
    q_message = Queue()  # 创建队列
    video_loader = VideoLoader(video_path, q_video, q_message)
    index = 0
    while index < 1000:
        frame = q_video.get()

        if index == 50:
            # 遗留问题，需要在外面清理管道
            q_message.put(3000)
            # clean_queue(q_video)
        print(index)
        index += 1

# test()
