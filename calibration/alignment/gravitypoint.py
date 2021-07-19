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
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    mu = cv2.moments(img_gray, True)
    gravitypoint_x, gravitypoint_y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])

    # 重心を画像で表示
    cv2.circle(img_gray, (gravitypoint_x, gravitypoint_y), 1, 100, 1, 3)
    plt.imshow(img_gray)
    plt.colorbar()
    plt.show()

    ic(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

def get_gravitypoint_img_gray(img_gray, isShow=False):
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
    if isShow:
        plt.show()

    ic(gravitypoint_x, gravitypoint_y)
    return gravitypoint_x, gravitypoint_y

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
def getgp(img, threshold):
    ret, gray = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    invgray = cv2.bitwise_not(gray)
    get_gravitypoint_img_gray(invgray)

if __name__ == '__main__':
    # dir_path = '/Users/paix/Desktop/Python_lab/calibration/alignment/img/projection_accuracy/'
    # dir_path = '/Users/paix/Desktop/Python_lab/frame_data/20210421/projection/'# 20210421のデータ
    dir_path = '/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/'# 20210706のデータ
    CMOS_path = dir_path + 'CMOS_date.bmp'
    pyrometer_path = dir_path + 'pyrometer_date.bmp'
    CMOS_thresh = 115
    pyro_thresh = 75
    # [min_y:max_y, min_x:max_x,RGB]
    ic('補正点:左上')
    img = cv2.imread(CMOS_path)[347:397, 161:224, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[174:192, 246:270, 1]
    getgp(img,pyro_thresh)

    ic('補正点:右上')
    img = cv2.imread(CMOS_path)[344:394, 463:528, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[175:195, 336:355, 1]
    getgp(img,pyro_thresh)

    ic('補正点:右下')
    img = cv2.imread(CMOS_path)[545:595, 446:517, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[238:259, 333:354, 1]
    getgp(img,pyro_thresh)

    ic('補正点:左下')
    img = cv2.imread(CMOS_path)[539:585, 159:230, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[235:252, 253:274, 1]
    getgp(img,pyro_thresh)

    ic('評価点:中心')
    img = cv2.imread(CMOS_path)[429:484, 318:381, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[202:222, 294:315, 1]
    getgp(img,pyro_thresh)

    ic('評価点:上')
    img = cv2.imread(CMOS_path)[228:280, 288:350, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[135:155, 285:308, 1]
    getgp(img,pyro_thresh)

    ic('評価点:下')
    img = cv2.imread(CMOS_path)[608:660, 303:386, 0]
    getgp(img, CMOS_thresh)
    img = cv2.imread(pyrometer_path)[259:276, 294:321, 1]
    getgp(img,pyro_thresh)