# coding:utf-8
import sys
import cv2
import os
from bitstring import ConstBitStream, BitStream


# if len(sys.argv) < 3:
#     print("Please input video path!")
# else:
#     video_path = sys.argv[1]
#     jpg_save_path = video_path[0:-4] + '_jpg'
#     decode = sys.argv[2]#第二个参数表示视频格式，4为H264，5为H265
#     print("video_path:" + video_path)
#     print("jpg_path:" + jpg_save_path)

# if not os.path.exists(jpg_save_path):
#     os.makedirs(jpg_save_path)
def get_video_time(video_path, decode=5):
    '''
        H264 SEI自定义格式
        sei_flag 0x0000 0001 06
        unsigned char byType;     //sei数据类型,为06
        unsigned char byRes1[4];  //预留
        unsigned int  dwSec;      //秒,UTC
        unsigned int  dwNan;      //纳秒部分
        ……后面略去，此处只关心时间戳位置
    '''

    '''
        H265 SEI自定义格式
        sei_flag 0x0000 0001 4e01
        unsigned char byType;     //sei数据类型,为06
        unsigned char byRes1[4];  //预留
        unsigned int  dwSec;      //秒,UTC
        unsigned int  dwNan;      //纳秒部分
        ……后面略去，此处只关心时间戳位置
    '''
    mp4_data = ConstBitStream(filename=video_path)

    if decode == 4:
        sei_start = '0x000000010606'  # sei开始标志,天准自定义格式
        time_bytes = 10
    elif decode == 5:
        sei_start = '0x000000014e0106'  # sei开始标志,天准自定义格式
        time_bytes = 11

    sei_starts = mp4_data.findall(sei_start, bytealigned=True)  # 一次找到全部符合的
    time_secs = []
    time_nans = []
    time_floats = []
    for sei_start in sei_starts:
        time_index = sei_start + time_bytes * 8  # 从sei_start往后数time_bytes个字节即为时间戳开始位置
        mp4_data.pos = time_index
        time_sec = mp4_data.read("uint:32")
        time_nan = mp4_data.read("uint:32")

        time_secs.append((str)(time_sec))
        if time_nan == 768:  # 当ns时间为000 000 030时，读出来会是768的奇怪bug，暂时规避
            time_nan = 30
        time_nans.append((str)(time_nan))
        time_float = float(time_sec) + float(time_nan) / 1000000000
        time_floats.append(time_float)
    return [time_secs, time_nans, time_floats]
    # 1673422 834 833333347
    # 1673422 476 166666680
    # 0000000 358 766666666


if __name__ == '__main__':
    input_dir = r'/home/nailinliao/Desktop/camera1/1670812712066666690.mp4'

    get_video_time(input_dir, decode=5)
