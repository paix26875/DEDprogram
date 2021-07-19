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

def get_gravitypoint_img(img_color, show_gp_img = True):
    """
    カラー画像の輪郭から重心を求める

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
    # img_color = [img_color[:,:,2],img_color[:,:,1],img_color[:,:,0]]
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    mu = cv2.moments(img_gray, True)
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    if show_gp_img == True:
        # 重心を画像で表示
        # cv2.circle(img_gray, (gravitypoint_x, gravitypoint_y), 1, 100, 1, 3)
        cv2.rectangle(img_color, (gravitypoint_x-10, gravitypoint_y-10),(gravitypoint_x+10, gravitypoint_y+10),(0,255,0))
        plt.imshow(img_color)
        # plt.colorbar()
        plt.show()

    ic(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

def get_gravitypoint_img_gray(img_gray):
    """
    グレースケール画像の輪郭から重心を求める

    Parameters
    ----------
    img_gray : numpy
        画像のRGB値が入った配列
    
    Returns
    -------
    gravitypoint_x : int
        重心のx座標
    gravitypoint_y : int
        重心のy座標
    """
    mu = cv2.moments(img_gray, True)
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    # 重心を画像で表示
    cv2.circle(img_gray, (gravitypoint_x, gravitypoint_y), 1, 100, 1, 3)
    plt.imshow(img_gray)
    plt.colorbar()
    plt.show()

    ic(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

def get_gravitypoint_CMOS(img_color, show_gp_img = True, threshold = 20, print_gp = True):
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
    
    img_red = img_color[:,:,0]
    ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
    # cv2.imshow("image", img_thresh)
    # cv2.waitKey(0)

    mu = cv2.moments(img_thresh, False)
    if mu["m00"] == 0:
        gravitypoint_x = 74
        gravitypoint_y = 264
        return gravitypoint_x, gravitypoint_y
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    if show_gp_img == True:
        # 重心を画像で表示
        cv2.circle(img_thresh, (gravitypoint_x, gravitypoint_y), 1, 100, 1, 3)
        plt.imshow(img_thresh)
        plt.colorbar()
        plt.show()
    if print_gp:
        ic(gravitypoint_x, gravitypoint_y)
    if gravitypoint_y > 700 or gravitypoint_x < 200:
        gravitypoint_x = 300
        gravitypoint_y = 500
        return gravitypoint_x, gravitypoint_y
    return gravitypoint_x, gravitypoint_y

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
    dir_path = '/Users/paix/Desktop/Python_lab/calibration/alignment/img/projection_accuracy/'
    CMOS_path = dir_path + 'CMOS_date.bmp'
    pyrometer_path = dir_path + 'pyrometer_date.bmp'
    img = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20210421/CMOS/before_projection/1600/img_86.bmp")
    x,y = get_gravitypoint_CMOS(img, threshold=25)
    img = img[y - 45:y + 45, x - 60:x + 60, 0:3]
    cv2.imwrite("/Users/paix/Documents/Research/M2打ち合わせ/第2回資料/CMOS_1600_before86trimmed.bmp", img)
    # 左上
    # img = cv2.imread(CMOS_path)[1350:1420, 1400:1500, 0:3]
    # img = cv2.imread(pyrometer_path)[110:140, 140:165, 0:3]

    # 右上
    # img = cv2.imread(CMOS_path)[880:980, 1880:1960, 0:3]
    # img = cv2.imread(pyrometer_path)[110:140, 400:430, 0:3]

    # 右下
    # img = cv2.imread(CMOS_path)[1130:1210, 2660:2730, 0:3]
    # img = cv2.imread(pyrometer_path)[300:325, 400:430, 0:3]

    # 左下
    # img = cv2.imread(CMOS_path)[1650:1760, 2260:2340, 0:3]
    # img = cv2.imread(pyrometer_path)[295:320, 140:170, 0:3]


    # # get_gravitypoint_contour(img)
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # invgray = cv2.bitwise_not(gray)

    # get_gravitypoint_img_gray(invgray)
    
    # img_path = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp"
    # img = cv2.imread(img_path)
    # get_gravitypoint_CMOS(img)
    