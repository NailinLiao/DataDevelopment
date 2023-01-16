import os
import random
import shutil

base_file_path = r'C:\Users\NailinLiao\Desktop\单帧车载电源动态\camera'
camera_list = ['camera1', 'camera2', 'camera3']
save_path = r'C:\Users\NailinLiao\Desktop\ret'
Random_len = 300
partition = 3


def get_random_file_list(get_path, Random_len):
    file_name_list = os.listdir(get_path)
    random_file_name_list = random.sample(file_name_list[10000:], Random_len)
    return random_file_name_list


def chunks(origin_list, n):
    if len(origin_list) % n == 0:
        cnt = len(origin_list) // n
    else:
        cnt = len(origin_list) // n + 1

    for i in range(0, n):
        yield origin_list[i * cnt:(i + 1) * cnt]


def main():
    random_file_name_list = get_random_file_list(os.path.join(base_file_path, 'camera1'), Random_len)
    chunks_list = chunks(random_file_name_list, partition)

    for index, chunk in enumerate(chunks_list):
        save_chunk = os.path.join(save_path, str(index))
        if not os.path.exists(save_chunk):
            os.makedirs(save_chunk)

        for file in chunk:
            for camera in camera_list:
                img_path = os.path.join(base_file_path, camera, file)
                img_name = str(file).split('.')[0] + '_' + str(camera) + '.png'
                shutil_path = os.path.join(save_chunk, img_name)
                print('Copy:', img_path, '  To  ', shutil_path)
                try:
                    shutil.copy(img_path, shutil_path)
                except:
                    print('Erro:', img_path)


if __name__ == '__main__':
    main()
