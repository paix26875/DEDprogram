# from get_meltpool_index import convert_img_to_numpy
# from get_meltpool_index import count_file_in_dir
# from get_meltpool_index import is_valid_meltpool_img
from get_meltpool_index import *
import time
from PIL import Image
import numpy as np
import os

if __name__ == '__main__':
    dir_path = 'frame_data/20200823/with_dwell_40/'
    frames = count_file_in_dir(dir_path)
    print(frames)
    meltpool_img_index = np.array([])
    meltpool_img_index_list = meltpool_img_index.tolist()

    for frame in range(frames):# 0.004

        img = Image.open(dir_path + 'sample_video_img_' + str(frame) + '.bmp')# 0.0004
        w, h= img.size
        img = img.crop((w/2, 0, w/2+1, h))# 0.003
        img_r = convert_img_to_numpy(img)# e-05

        if is_valid_meltpool_img(img_r):# e-5
            meltpool_img_index_list.append(frame)# e-07
            
    meltpool_img_index = np.asarray(meltpool_img_index_list)
    print(meltpool_img_index)