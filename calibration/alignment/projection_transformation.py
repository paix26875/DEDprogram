# https://sorabatake.jp/8713/
# import cv2
# import numpy as np
from icecream import ic
import os, json, math, cv2
from PIL import Image
from skimage import io
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

def projection_matrix(src_plts, dst_plts):
    """
    射影変換の変換マトリクスを算出する

    Parameters
    ----------
    src_plts : numpy
        変換前の4つの補正点座標
    dst_plts : numpy
        変換後の4つの補正点座標
    
    Returns
    -------
    projection_mat : numpy
        射影変換の変換マトリクス
    """
    projection_mat = cv2.getPerspectiveTransform(src_plts, dst_plts)
    ic(projection_mat)
    return projection_mat

def img_change_color(img,color):
    """
    画像を単一の色に変換する

    Parameters
    ----------
    img : numpy
        変換前の画像配列
    color : str
        変換後の色を指定
    
    Returns
    -------
    変換後の単一画像を返す
    """
    # 色変換
    TYPE_BLUE = 1
    TYPE_RED = 2
    if color == "blue":
        colortype = 1
    elif color == "red":
        colortype = 2
    temp_img = cv2.split(img)
    
    # ゼロ埋めの画像配列
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1
    zeros = np.zeros((height, width), img.dtype)
    #TYPE_BLUEだったら青だけ、それ以外（TYPE_RED）だったら赤だけ残し、他をゼロで埋める
    if colortype == TYPE_RED:
        return cv2.merge((temp_img[1],zeros,zeros))
    elif colortype == TYPE_BLUE:
        return cv2.merge((zeros,zeros,temp_img[1]))

def img_overray(img1, img2, accuracy):
    """
    画像を合成する

    Parameters
    ----------
    img1 : numpy
        合成する画像配列
    img2 : numpy
        合成する画像配列
    accuracy : int
        変換後の色を指定
    
    Returns
    -------
    saveimg : numpy
        合成後の画像を返す
    """
    img_merge = cv2.addWeighted(img1, 1, img2, 1, 0)
    
    height, width, channels = img_merge.shape[:3]

    saveimg = np.zeros((height, width, 3), np.uint8)
    
    for x in range(height):
        for y in range(width):
            b = img_merge[x,y,0]
            g = img_merge[x,y,1]
            r = img_merge[x,y,2]
            
            if (r > b-accuracy and r < b+accuracy): 
                saveimg[x,y] = [b,b,b]
            else :
                saveimg[x,y] = [r,g,b]
    return saveimg


if __name__ == '__main__':
    # #変換前の4点の座標
    # src_pts = np.array([[304, 711], [370, 638], [992, 492], [609, 1046]], dtype=np.float32)
    # #変換後の4点の座標
    # dst_pts = np.array([[290, 188], [326, 189], [455, 291], [196,276]], dtype=np.float32)
# x: 78, y: 54, x: 16, y: 6
# x: 72, y: 39, x: 17, y: 6
# x: 59, y: 49, x: 13, y: 10
# x: 93, y: 46, x: 14, y: 10
    #変換前の4点の座標[y, x]
    src_pts = np.array([[190,374], [490,370], [477,572], [192,564]], dtype=np.float32)
    #変換後の4点の座標
    dst_pts = np.array([[258,185], [345,187], [342,250], [262,245]], dtype=np.float32)
    mat = projection_matrix(src_pts, dst_pts)

    print("射影変換したい画像のパスを入力してください")
    # dir_name = input()
    path_name = input()
    path_name =  + 'img_' + str(i) + '.bmp'
    ic(path_name)
    img = cv2.imread(path_name)
    h, w, c = img.shape
    perspective_img = cv2.warpPerspective(img, mat, (w, h))

    # plt.imshow(img)
    # plt.show()
    # plt.imshow(perspective_img[:400, :640])
    # plt.show()
    os.makedirs('/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/' + filter + '/' + str(laser) + '/', exist_ok=True)
    cv2.imwrite('/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/' + filter + '/' + str(laser) + '/' + 'img_' + str(i) + '.bmp', perspective_img[0 : 480, 0 : 640, 0:3])