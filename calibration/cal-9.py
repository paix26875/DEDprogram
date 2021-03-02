# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:24:49 2020

@author: paix
"""

from PIL import Image
import sys, time
import numpy as np
import csv
import cv2
from function_for_calib import ave_filter
from matplotlib import pyplot as plt
POWER=1400#レーザ出力指定
# FRAME=136#1800Wのフレーム数指定
if (POWER == 1400):
    # 1400
    img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1400/img_181.bmp')
    img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1400-181-3908.BMP')
    O_TEMP_Y=200
    O_TEMP_X=280
    O_USB_Y=O_TEMP_Y
    O_USB_X=O_TEMP_X-14
    height=70
    width=70
elif(POWER == 1600):
    # 1600
    img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp')
    img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1600-164-3805.BMP')
    O_TEMP_Y=200
    O_TEMP_X=280
    O_USB_Y=193
    O_USB_X=267
    height=70
    width=60
elif(POWER == 1800):
    img_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1800/img_177.bmp')
    img_temp_all = Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1800-177-3813.BMP')
    O_TEMP_Y=200
    O_TEMP_X=280
    O_USB_Y=O_TEMP_Y
    O_USB_X=O_TEMP_X-14
    height=70
    width=70
    # if(FRAME == 141):
    #     # 1800-141
    #     img_all = Image.open('data/perspective/result_1800high/opencv_perspective_dst141.bmp')
    #     img_temp_all = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1800W_141_2835/全温度.bmp')
    #     O_TEMP_Y=310
    #     O_TEMP_X=270
    #     O_USB_Y=314
    #     O_USB_X=125
    #     height=30
    #     width=40
    # elif(FRAME == 140):
    #     #1800-140
    #     img_all = Image.open('data/perspective/result_1800high/opencv_perspective_dst140.bmp')
    #     img_temp_all = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1800W_140_2508/全温度.bmp')
    #     O_TEMP_Y=310
    #     O_TEMP_X=270
    #     O_USB_Y=314
    #     O_USB_X=125
    #     height=30
    #     width=40
    # elif(FRAME == 136):
    #     #1800-136
    #     img_all = Image.open('data/perspective1/result_1800highopencv_perspective_dst136.bmp')
    #     img_temp_all = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1800W_136_1465/全温度.bmp')
    #     O_TEMP_Y=291
    #     O_TEMP_X=124
    #     O_USB_Y=291
    #     O_USB_X=124
    #     height=100
    #     width=100
    
RGBvalue = 0
#kernel = 1/9*np.ones(3,3)
temp_b = [160, 10, 188, 248, 144, 40, 207, 239, 118, 71, 222, 255]
temp = 1400
TEMP = np.reshape(np.zeros(height*width),(height,width))
x = np.zeros(13)
y = np.zeros(13)
temp_y = np.zeros(13)

if __name__ == '__main__':
    #CMOS画像読み込み
    img_all_np = np.array(img_all)
    CMOS = img_all_np[O_USB_Y:O_USB_Y+height, O_USB_X:O_USB_X+width, RGBvalue]#90×90の配列にするかつRを抜き出す（第3引数）
    
    #温度画像読み込み
    #img = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1600W_92_2257/'+str(TEMPERATURE)+'.bmp')
    img_temp_np = np.array(img_temp_all)#画素値numpy化
    img_temp_b=img_temp_np[O_TEMP_Y:O_TEMP_Y+height, O_TEMP_X:O_TEMP_X+width,2]#90×90の配列にする                      
    for i in range(12):
        img_temp_single=np.where(img_temp_b == temp_b[i],temp,0)#
        TEMP += img_temp_single
        temp += 100
    #print(TEMP)
    """
    for i in range(1,78):
        for j in range(1,88):
            CMOS_ave = (CMOS[i,j] + CMOS[i,j+1] + CMOS[i+1,j] + CMOS[i+1,j+1] + CMOS[i-1,j-1] + CMOS[i-1,j] + CMOS[i-1,j+1] + CMOS[i,j-1] + CMOS[i+1,j-1])/9
            TEMP_ave = (TEMP[i,j] + TEMP[i,j+1] + TEMP[i+1,j] + TEMP[i+1,j+1] + TEMP[i-1,j-1] + TEMP[i-1,j] + TEMP[i-1,j+1] + TEMP[i,j-1] + TEMP[i+1,j-1])/9
            x = np.append(x,CMOS_ave)
            y = np.append(y,TEMP_ave)
    """
    x = np.reshape(ave_filter(CMOS),(height*width,))
    y = np.reshape(ave_filter(TEMP),(height*width,))
    np.savetxt('/Users/paix/Desktop/Python_lab/calibration/caldata/' + str(RGBvalue)+'_' + str(POWER) + '.csv', x)
    np.savetxt('/Users/paix/Desktop/Python_lab/calibration/caldata/' + str(POWER)+'.csv', y)
    xmat = ave_filter(CMOS)
    ymat = ave_filter(TEMP)
    
    #x = x[13:]
    #y = y[13:]
    xnew = np.arange(20,70,5)
    ynew = np.zeros(13)
    #plt.plot(x, y, 'o')
    for R in range (20,70,5):
        sum=0
        n=0
        for i in range ((width-3)*(height-3)):
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
    
    #ｘ、ｙを逆にするとき使う
    xold = ynew
    yold = xnew
    xnew = xold
    ynew = yold
    
    plt.plot(xnew, ynew, 'o')
    #a,b = np.polyfit(xnew, ynew, 1)
    a=17.13
    b=591.48
    yfit = a*xnew + b
    #plt.plot(xnew, yfit , '-') 
    yave = np.mean(ynew)#平均値
    sum_all = 0
    sum_fit = 0
    for i in range(9):
        sum_all += (ynew[i] - yave)**2
        sum_fit += (yfit[i] - yave)**2
    R2 = sum_fit/sum_all
    print(round(R2, 4))
    print("T = " + str(round(a,2)) + "R+" + str(round(b,2)))
        
    plt.show()
    #xr = np.reshape(x,(79,89))
    #yr = np.reshape(y,(79,89))
