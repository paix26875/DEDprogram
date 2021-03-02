# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 03:35:39 2019

@author: paix
参考記事：https://note.nkmk.me/python-opencv-video-to-still-image/
"""

import cv2
import os
import numpy as np
# import skvideo.io #追加

def saveAllFrames(video_path, dir_path, basename, ext='bmp'):
    """
    動画をフレームに切り出して指定ディレクトリに保存

    Parameters
    -----------
    video_path:str
        切り出したい動画の相対パスを指定
    dir_path:str
        切り出したフレームを保存するディレクトリ名
    basename:str
        切り出したフレームの連番の前につく名前を指定
    ext:str
        切り出したフレームの拡張子を指定。デフォルト値はbmp
    """
    cap = cv2.VideoCapture(video_path)
    # reader = skvideo.io.FFmpegReader(video_path) #追加

    if not cap.isOpened():
        return
    
    # dir_pathという名前のディレクトリ作成（すでに存在している場合はスルーされる）
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    # digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
    # for frame in reader.nextFrame(): #追加
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n), ext), frame)
            n += 1
        else:
            return

# mac
# saveAllFrames('raw_data/20201123/10/CMOS/1800.avi', 'frame_data/20201123/10/1800', 'img')
saveAllFrames('raw_data/20201123/perspective10/9,10.avi', 'frame_data/20201123/10/perspective', 'img')


# windows
# saveAllFrames('C:/Users/paix/Desktop/実験データ/20200217/'+str(POWER)+'W.avi', 'data/temp/2020_0217/result_'+str(POWER)+'W', 'img')
