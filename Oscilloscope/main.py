import cv2
import numpy as np
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from io import BytesIO
from PIL import Image
import pandas as pd

'''
show video and Oscilloscope
'''


def show_video(cap, index):
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    _, frame = cap.read()
    cv2.imshow('frame', frame)


def show_oscilloscope(data_list: list, index: int, step=50, sr=30):
    head = index - step
    end = index + step
    show_oscilloscope_list = data_list[head:end]

    # time = np.arange(0, len(show_oscilloscope_list)) * (1.0 / sr)
    time = np.arange(head, end)
    y = np.mean(show_oscilloscope_list[step:step + 1])
    x = time[step]
    text = 'frame index:' + str(index) + '___value:' + str(y)
    plt.text(x, y, text, ha='left', wrap=True)
    plt.scatter(y=show_oscilloscope_list[step:step + 1], x=time[step:step + 1], s=10, )
    plt.plot(time, show_oscilloscope_list)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_img = Image.open(buffer)
    data_img = np.array(data_img)

    cv2.imshow('oscilloscope_', data_img)
    plt.clf()


def show(data_list, index, video_path, cap=0, step=50):
    show_oscilloscope(data_list, index, step)

    if video_path != None:
        # cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        # _, frame = cap.read()
        # cv2.imshow('frame', frame)
        show_video(cap, index)


def main(ins_data, video_path=None, show_oscilloscope_len=100):
    DataFrame = pd.read_csv(ins_data)
    data_list = DataFrame['Front_Axle_Speed']

    data_len = len(data_list)
    step = int(show_oscilloscope_len / 2)
    cap = 0
    if video_path != None:
        cap = cv2.VideoCapture(video_path)

    index = step
    run = True
    while index + step < data_len:
        if run:
            show(data_list, index, video_path, cap, step)
            index += 1

        key = cv2.waitKey(1)
        if key == 32:
            run = bool(1 - run)
        elif key == 27:
            break
        elif key == 81:
            index -= 1
            show(data_list, index, video_path, cap)
        elif key == 83:
            index += 1
            show(data_list, index, video_path, cap)


if __name__ == '__main__':
    video_path = r'/home/nailinliao/Desktop/camera1/1670812712066666690.mp4'
    ins_data = r'/home/nailinliao/Desktop/radar1/1670812712096032405_EBC2_EBS.csv'
    # DataFrame = pd.read_csv(ins_data)
    # data_list = DataFrame['Front_Axle_Speed']
    main(ins_data, video_path)
