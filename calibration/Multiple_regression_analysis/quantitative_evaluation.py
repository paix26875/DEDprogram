import cv2
from PIL import Image
import numpy as np
from icecream import ic
import gravitypoint as gp
import trimming as tr
import twocolor_convert as tc
from matplotlib import pyplot as plt
import os
import pandas as pd


# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)

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
    # ic([len(v) for v in temp_img])
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ゼロ埋めの画像配列
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1
    zeros = np.zeros((height, width), img.dtype)
    #TYPE_BLUEだったら青だけ、それ以外（TYPE_RED）だったら赤だけ残し、他をゼロで埋める
    # グレースケールでやってみたい。これだと赤がゼロのところはゼロになっちゃう
    # if colortype == TYPE_RED:
    #     return cv2.merge((temp_img[1],zeros,zeros))
    # elif colortype == TYPE_BLUE:
    #     return cv2.merge((zeros,zeros,temp_img[1]))
    if colortype == TYPE_RED:
        return cv2.merge((img_gray,zeros,zeros))
    elif colortype == TYPE_BLUE:
        return cv2.merge((zeros,zeros,img_gray))

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
    # レーザ出力とフレーム数の設定
    print('laser power? 1400 / 1600 / 1800')
    laser_power = int(input())
    frames = 100
    RGBvalue = 0
    height = 90
    width = 120
    RGBmin = 25
    RGBmax = 255

    # pathの設定
    color_img_path = 'calibration/time_average/colorimg/20210421/' + str(laser_power) + "_101.bmp"
    if os.path.exists(color_img_path):
        img_pil = Image.open(color_img_path)
        pyro_np = np.array(img_pil)
        temperature_ave = tc.totemperature(pyro_np)
        pyro_x, pyro_y = gp.get_gravitypoint_img(pyro_np)
        pyro_temp_g = temperature_ave
        TEMP = temperature_ave# 次元配列
        TEMPplt = temperature_ave.reshape(90*120)# 2次元配列
        # # # 温度ヒストグラム表示
        # plt.hist(TEMPplt, color="red", bins=128)
        # plt.ylim(0, 200)
        # plt.xlim(1300, 3000)
        # plt.xlabel("temperature")
        # plt.show()
    


    # print('after / before projection?')
    # afbf = input()
    afbf = 'after'
    # print('Average range')
    # average = int(input())
    average=10
    save_name = str(laser_power) + "_RGB.bmp"
    threshold = 20
    
    # pathの設定
    color_img_path = '/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/temp/CMOS_raw_int8_RGBmin' + str(average) + afbf + str(threshold) + save_name
    if os.path.exists(color_img_path):
        img_pil = Image.open(color_img_path)
        CMOS_np = np.array(img_pil)
        temperature_ave = tc.totemperature(CMOS_np)
        CMOS_x, CMOS_y = gp.get_gravitypoint_img(CMOS_np)
        CMOS_temp_g = temperature_ave
        CMOS = temperature_ave# 2次元配列
        CMOSplt = temperature_ave.reshape(90*120)# 1次元配列
        # 温度ヒストグラム表示
        # plt.hist(CMOSplt, color="blue", bins=128)
        # plt.ylim(0, 200)
        # plt.xlim(1300, 3000)
        # plt.xlabel("temperature")
        # plt.show()

    for area in range(5, 30, 5):
        pyro_g = pyro_temp_g[ pyro_y - area : pyro_y + area , pyro_x - area : pyro_x + area]
        CMOS_g = CMOS_temp_g[ CMOS_y - area : CMOS_y + area , CMOS_x - area : CMOS_x + area]
        ic(np.mean(CMOS_g) - np.mean(pyro_g))
    ic(np.count_nonzero(CMOS >= 1300))
    ic(np.count_nonzero(TEMP >= 1300))
    
    TEMP=TEMP[CMOS>1300]
    # print(TEMP.shape)
    CMOS=CMOS[CMOS>1300]
    CMOS=CMOS[TEMP>1300]
    TEMP=TEMP[TEMP>1300]
    
    ERROR = abs(TEMP - CMOS)
    ic(np.max(ERROR))
    ic(np.mean(ERROR))
    ic(np.median(ERROR))
    step = 10
    for t in range(1300, 2600 ,step):
        index = np.median(ERROR[(TEMP >= t) & (TEMP < t+step)])
        # ic(t)
        # ic(index)
        


    ERRORplt = TEMPplt - CMOSplt
    plt.hist(ERROR, color="red", bins=128)
    plt.xlabel("temperature")
    # plt.show()
    # ERROR = ERROR / np.max(ERROR) * 255
    # print(ERROR)
    # cv2.imshow('image', ERROR)
    # cv2.waitKey(0)

    # x, y = gp.get_gravitypoint_img(CMOS_np)
    # ic(x)
    # ic(y)
    # CMOS_np = CMOS_np[ y - 44 : y + 30 , x - 60 : x + 60, 0:3]
    # x, y = gp.get_gravitypoint_img(pyro_np)
    # ic(x)
    # ic(y)
    # pyro_np = pyro_np[ y - 44 : y + 30 , x - 60 : x + 60, 0:3]
    # # 温度のピクセル数の差を出す方がいいかも
    # print(CMOS.shape)
    # # 重ね合わせ
    # CMOS_red = img_change_color(CMOS_np, "blue")
    # pyrometer_blue = img_change_color(pyro_np, "red")
    
    # img_compare = img_overray(CMOS_red, pyrometer_blue, 30)
    # cv2.imwrite("/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/temp/img_compare" + str(laser_power) + ".bmp", img_compare)
    # step = 10
    error_count = np.array([])
    for t in range(1300, 2600 ,step):
        CMOS_count = np.count_nonzero((CMOS >= t) & (CMOS < t+step))
        TEMP_count = np.count_nonzero((TEMP >= t) & (TEMP < t+step))
        error_count = abs(np.append(error_count, CMOS_count - TEMP_count))
        # ic(CMOS_count)
        # ic(TEMP_count)
        # ic(error_count)
    x = np.arange(1300, 2600 ,step)
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ax.bar(x, error_count)
    # plt.show()