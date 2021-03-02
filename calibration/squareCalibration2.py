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

# 1400
# O_TEMP_Y=200
# O_TEMP_X=280
# O_USB_Y=O_TEMP_Y
# O_USB_X=O_TEMP_X
# height=70
# width=70

# 1600
# O_TEMP_Y=200
# O_TEMP_X=280
# O_USB_Y=193
# O_USB_X=267
# height=70
# width=60

# 1800
O_TEMP_Y=200
O_TEMP_X=280
O_USB_Y=O_TEMP_Y
O_USB_X=O_TEMP_X-14
height=70
width=70

RGBvalue = 2
#kernel = 1/9*np.ones(3,3)
temp_b = [160, 10, 188, 248, 144, 40, 207, 239, 118, 71, 222, 255]
temp = 1400
TEMP = np.reshape(np.zeros(height*width),(height,width))
x = np.zeros(13)
y = np.zeros(13)

rmax = 65

if __name__ == '__main__':
    #CMOS画像読み込み
    # img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1400/img_181.bmp')
    # img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp')
    img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1800/img_177.bmp')
    img_all_np = np.array(img_all)
    CMOS = img_all_np[O_USB_Y:O_USB_Y+height, O_USB_X:O_USB_X+width, RGBvalue]#90×90の配列にするかつRを抜き出す（第3引数）
    xxx = CMOS
    #温度画像読み込み
    # img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1400-181-3908.BMP')
    # img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1600-164-3805.BMP')
    img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1800-177-3813.BMP')
    img_temp_np = np.array(img_temp_all)#画素値numpy化
    img_temp_b=img_temp_np[O_TEMP_Y:O_TEMP_Y+height, O_TEMP_X:O_TEMP_X+width,2]#90×90の配列にする                      
    for i in range(12):
        img_temp_single=np.where(img_temp_b == temp_b[i],temp,0)#
        TEMP += img_temp_single
        temp += 100
    yyy = TEMP
    #print(TEMP)
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
    x = x[13:]
    y = y[13:]
    xnew = np.arange(25,rmax,5)
    ynew = np.zeros(13)
    #plt.plot(x, y, 'o')
    for R in range (25,rmax,5):
        sum=0
        n=0
        for i in range ((height-1)*(width-1)):
            if y[i] !=0 and x[i] !=0:
                if x[i]<R+3 and x[i]>R-2:
                    sum += y[i]
                    n += 1
        print(n)
        if n != 0:
            ynew = np.append(ynew,sum/n)
        else:
            ynew = np.append(ynew,0)
    ynew = ynew[13:]
    print("ynewの値")
    print(np.shape(ynew))
    print(ynew)
    """
    #ｘ、ｙを逆にするとき使う
    xold = ynew
    yold = xnew
    xnew = xold
    ynew = yold
    """
    plt.plot(xnew, ynew, 'o')
    a,b = np.polyfit(xnew, ynew, 1)
    yfit = a*xnew + b
    # yfit = 9.48*xnew + 1118.38
    # 1600のキャリブレーション値
    # yfit = 4.99*xnew + 707.7
    plt.plot(xnew, yfit , '-') 
    yave = np.mean(ynew)#平均値
    sum_all = 0
    sum_fit = 0
    xlength = int((rmax-25)/5)
    for i in range(xlength):
        # sum_all += (ynew[i] - yave)**2
        # sum_fit += (yfit[i] - yave)**2
        sum_all += (ynew[i] - yave)**2
        sum_fit += (ynew[i] - yfit[i])**2
    R2 = 1 - sum_fit/sum_all
    print(R2)
    print("T = " + str(round(a,2)) + "R+" + str(round(b,2)))
    
    #xr = np.reshape(x,(79,89))
    #yr = np.reshape(y,(79,89))
    plt.show()