# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:18:17 2019

@author: paix
"""
"""""""""""""""""""""
射影変換②用プログラム

"""""""""""""""""""""
import cv2
import numpy as np
from imgIndexMeltpool import countFile


#変換前の4点の座標
# src_pts = np.array([[210, 876], [268, 794], [383, 833], [342, 910]], dtype=np.float32)
src_pts = np.array([[304, 711], [370, 638], [992, 492], [609, 1046]], dtype=np.float32)
#変換後の4点の座標
# dst_pts = np.array([[291, 189], [326, 189], [324, 212], [291,211]], dtype=np.float32)
# dst_pts = np.array([[290, 188], [326, 189], [454, 285], [195,286]], dtype=np.float32)
dst_pts = np.array([[290, 188], [326, 189], [455, 291], [196,276]], dtype=np.float32)
mat = cv2.getPerspectiveTransform(src_pts, dst_pts)
print(mat)
# [[ 5.42651593e-01  2.04362225e-01  2.00000000e+01]
#  [-9.38078109e-02  8.04156675e-01  5.00000000e+01]
#  [-9.40390545e-04  1.42057782e-03  1.00000000e+00]]

dirname = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/"
filenum = countFile(dirname + "1800")
print(filenum)

for i in range(1, filenum):
    n = i-1
    # 変換したい画像のパス
    img = cv2.imread(dirname + "1800/img_" + str(n) + ".bmp")
    h, w, c = img.shape
    perspective_img = cv2.warpPerspective(img, mat, (w, h))
    # 変換後の画像のパス
    cv2.imwrite(dirname + "afterper2/1800/img_" + str(n) + '.bmp', perspective_img)


# KAKUTYOUSHI='.bmp'
# i=183#画像番号
# JOUKEN='2000high'
# img = cv2.imread('data/perspective/result_'+JOUKEN+'/opencv_perspective_dst'+str(i)+KAKUTYOUSHI)
# #print(img)
# h, w, c = img.shape
# #print(h, w, c)
# # 225 400 3

# perspective_img = cv2.warpPerspective(img, mat, (w, h))
# cv2.imwrite('data/perspective1/result_'+JOUKEN+'opencv_perspective_dst'+str(i)+KAKUTYOUSHI, perspective_img)
