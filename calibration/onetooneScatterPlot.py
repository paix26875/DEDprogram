# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:38:41 2020
2×2のキャリブレーションを行う
@author: paix
"""
from PIL import Image
import sys, time
import numpy as np
import csv
import cv2
from function_for_calib import ave_filter
from matplotlib import pyplot as plt
from icecream import ic
from matplotlib import cm
from matplotlib.ticker import MaxNLocator

# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)
"""
# 1400
O_TEMP_Y=270
O_TEMP_X=200
O_USB_Y=270
O_USB_X=200
height=130
width=130
"""
# # 1600
# O_TEMP_Y=290
# O_TEMP_X=200
# O_USB_Y=290
# O_USB_X=200
# height=80
# width=90
# 1600
O_TEMP_Y=200
O_TEMP_X=280
O_USB_Y=193
O_USB_X=267
height=70
width=60
"""
# 1800
O_TEMP_Y=310
O_TEMP_X=270
O_USB_Y=314
O_USB_X=125
height=30
width=40
"""

RGBvalue = 2
RGBmax = 255
RGBmin = 20
#kernel = 1/9*np.ones(3,3)
temp_b = [160, 10, 188, 248, 144, 40, 207, 239, 118, 71, 222, 255]
temp = 1400
TEMP = np.reshape(np.zeros(height*width),(height,width))
x = np.zeros(13)
y = np.zeros(13)

if __name__ == '__main__':
    ##############
    #画像の読み込み#
    ##############
    #CMOS画像読み込み
    #img_all = Image.open('data/perspective1/result_1400highopencv_perspective_dst135.bmp')
    # img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp')
    img_all = Image.open('/Users/paix/Desktop/Python_lab/dstName.bmp')
    #img_all = Image.open('data/perspective/result_1800high/opencv_perspective_dst141.bmp')
    img_all_np = np.array(img_all)
    CMOS = img_all_np[O_USB_Y:O_USB_Y+height, O_USB_X:O_USB_X+width, RGBvalue]#90×90の配列にするかつRを抜き出す（第3引数）
    xxx = CMOS

    #温度画像読み込み
    #img_temp_all = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1400W_135_2663/全温度.bmp')
    img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1600-164-3805.BMP')
    #img_temp_all = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1800W_141_2835/全温度.bmp')9
    img_temp_np = np.array(img_temp_all)#画素値numpy化
    img_temp_b=img_temp_np[O_TEMP_Y:O_TEMP_Y+height, O_TEMP_X:O_TEMP_X+width,2]#90×90の配列にする                      
    # 色（グラデーション）情報から温度情報に変換
    for i in range(12):
        img_temp_single=np.where(img_temp_b == temp_b[i],temp,0)#
        TEMP += img_temp_single
        temp += 100
    yyy = TEMP


    ##################
    #2×2の範囲で平均化##
    ##################
    """
    for i in range(height-1):
        for j in range(width-1):
            if CMOS[i,j] > 20:
                CMOS_ave = (CMOS[i,j] + CMOS[i,j+1] + CMOS[i+1,j] + CMOS[i+1,j+1])/4
                TEMP_ave = (TEMP[i,j] + TEMP[i,j+1] + TEMP[i+1,j] + TEMP[i+1,j+1])/4
                x = np.append(x,CMOS_ave)
                y = np.append(y,TEMP_ave)
            else:
                x = np.append(x,0)
                y = np.append(y,0)
    """
    ################
    #平均化しない場合##
    ################
    x = np.reshape(CMOS, height * width)
    y = np.reshape(TEMP, height * width)
    x = x[13:]
    y = y[13:]

    """
    #ｘ、ｙを逆にするとき使う
    xold = ynew
    yold = xnew
    xnew = xold
    ynew = yold
    """
    # グラフに表示するためにデータを整形していく
    # 非ゼロ要素の抽出 
    # ゼロ要素を含むと表示が小さくなったり近似する時に邪魔なので取り除く 
    result_rgb = x[y.nonzero()]
    result_temperature = y[y.nonzero()]
    # result_samplenumber = n[y.nonzero()]
    
    # xnew = result_rgb
    # ynew = result_temperature
    # nnew = result_samplenumber

    # 一次近似
    # a,b = np.polyfit(xnew, ynew, 1)
    # yfit = a*xnew + b
    # yfit = 9.48*xnew + 1118.38

    # 決定係数の算出
    # yave = np.mean(ynew)#平均値
    # sum_all = 0
    # sum_fit = 0
    # for i in range(ynew.size):
    #     sum_all += (ynew[i] - yave)**2
    #     sum_fit += (yfit[i] - yave)**2
    # R2 = sum_fit/sum_all

    ic(RGBvalue)
    # ic(R2)
    # print("T = " + str(round(a,2)) + "R+" + str(round(b,2)))
    

    ###########
    #結果の表示#
    ##########

    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

    # figureオブジェクトを作成
    fig = plt.figure()
    ax1 = fig.subplots()

    # ax1とax2を関連させる
    # ax2 = ax1.twinx()
    
    # それぞれのaxesオブジェクトのlines属性にLine2Dオブジェクトを追加
    ax1.plot(result_rgb, result_temperature, marker='.', color='blue', label="溶融池温度", linestyle='None')
    # ax1.plot(xnew, yfit, color='orange', label="一次近似")
    # ax2.plot(xnew, nnew, marker='.', color='red', label="サンプル数", linestyle='None')
    
    #凡例をつける
    ax1.legend()
    # ax2.legend()
    # # 結果のプロット
    # plt.plot(xnew, ynew, 'o')
    # plt.plot(xnew, nnew, 'o')

    
    plt.show()