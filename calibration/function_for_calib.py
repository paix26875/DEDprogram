# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:07:53 2020

@author: paix
"""
from PIL import Image
import sys, time
import numpy as np
import csv
import cv2


def ave_filter(gray):
    #gray = cv2.imread("data/perspective1/result_1600highopencv_perspective_dst92.bmp")
    
    # kernel of blur filter
    # カーネル（縦方向の輪郭検出用）
    kernel = np.array([[1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9]])
    
    # Spatial filtering
    # 方法2(OpenCVで実装)
    dst = cv2.filter2D(gray, -1, kernel)
    return dst
    # output
    # 結果を出力
    #cv2.imwrite("data/perspective1/gray.bmp", dst)