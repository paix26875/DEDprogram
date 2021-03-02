"""
重心を求める
参考記事：https://cvtech.cc/pycvmoment/
方法1：画像から重心を求める
方法2：輪郭から重心を求める
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic

def get_gravitypoint_img(img_color):
    """
    画像の輪郭から重心を求める

    Parameters
    ----------
    img_color : numpy
        画像のRGB値が入った配列
    
    Returns
    -------
    gravitypoint_x : int
        重心のx座標
    gravitypoint_y : int
        重心のy座標
    """
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    mu = cv2.moments(img_gray, True)
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    # # 重心を画像で表示
    # cv2.circle(img_gray, (gravitypoint_x, gravitypoint_y), 4, 100, 2, 4)
    # plt.imshow(img_gray)
    # plt.colorbar()
    # plt.show()

    ic(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

    pass

def get_gravitypoint_CMOS(img_color):
    """
    画像の輪郭から重心を求める(CMOS画像用)

    Parameters
    ----------
    img_color : numpy
        画像のRGB値が入った配列
    
    Returns
    -------
    gravitypoint_x : int
        重心のx座標
    gravitypoint_y : int
        重心のy座標
    """
    threshold = 20
    img_red = img_color[:,:,0]
    ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
    # cv2.imshow("image", img_thresh)
    # cv2.waitKey(0)

    mu = cv2.moments(img_thresh, False)
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    # # 重心を画像で表示
    # cv2.circle(img_thresh, (gravitypoint_x, gravitypoint_y), 4, 100, 2, 4)
    # plt.imshow(img_thresh)
    # plt.colorbar()
    # plt.show()

    ic(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

    pass

def get_gravitypoint_contour(img_color):
    """
    画像の輪郭から重心を求める

    Parameters
    ----------
    img_color : numpy
        画像のRGB値が入った配列
    
    Returns
    -------
    gravitypoint_x : int
        重心のx座標
    gravitypoint_y : int
        重心のy座標
    """
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    _, contours = cv2.findContours(img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # なんか2変数しか帰ってきてないみたい
    # _, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    maxCont=contours[0]
    for c in contours:
        if len(maxCont)<len(c):
            maxCont=c
    
    # cv2.moments関数の対応フォーマット：np.int8 or np.float32
    # maxContのフォーマットをnp.int32→np.float32に変更
    maxCont = np.array(maxCont, dtype=np.float32)
    mu = cv2.moments(maxCont)
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    # 重心を画像で表示
    cv2.circle(img_gray, (gravitypoint_x, gravitypoint_y), 4, 100, 2, 4)
    plt.imshow(img_gray)
    plt.colorbar()
    plt.show()

    print(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

if __name__ == '__main__':
    img_path = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1600-164-3805.BMP"
    img = cv2.imread(img_path)
    # get_gravitypoint_contour(img)
    get_gravitypoint_img(img)
    
    # img_path = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp"
    # img = cv2.imread(img_path)
    # get_gravitypoint_CMOS(img)
    