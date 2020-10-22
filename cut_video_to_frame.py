# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 03:35:39 2019

@author: paix
"""

import cv2
import os
import numpy as np

def save_all_frames(video_path, dir_path, basename, ext='bmp'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    #digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n), ext), frame)
            n += 1
        else:
            return
    
    
POWER=2000
# windows
# save_all_frames('C:/Users/paix/Desktop/実験データ/20200217/'+str(POWER)+'W.avi', 'data/temp/2020_0217/result_'+str(POWER)+'W', 'sample_video_img')


# mac

save_all_frames('raw_data/20200823/without_dwell_40.avi', 'frame_data/20200823/without_dwell_40', 'sample_video_img')

"""
FEEDRATE=np.array([50,60,70,75,80,85,90,95,100,105,110,115,120])    
if __name__ == '__main__':
    for i in range(0,13):
        FEED=FEEDRATE[i]
        save_all_frames('C:/Users/paix/Desktop/R_data_20200208/'+str(FEED)+'%.avi', 'data/temp/2020_0208/result_'+str(FEED)+'%', 'sample_video_img')
"""
    #save_all_frames('C:/Users/paix/Desktop/R_data_20200208/50%.avi', 'data/temp/2020_0208/result_50%', 'sample_video_img')

#save_all_frames('C:/Users/paix/Desktop/実験350・1200W7/1000W.avi', 'data/temp/result_png', 'sample_video_img', 'png')
