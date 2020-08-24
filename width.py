# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 03:53:45 2020

@author: paix
"""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
溶融池の幅測定
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""
処理時間計測
"""""""""""""""
#-*- using:utf-8 -*-
import time
import sys, time
import numpy as np
import csv
from matplotlib import pyplot as plt
from PIL import Image
from scipy.interpolate import interp1d
from Automatic_Detection import auto_detection
from Automatic_Detection import meltpool_width

def array_info(x):
    print("配列のshape", x.shape)
    print("配列の要素のデータ型", x.dtype)
    print("配列の中身\n",x,"\n")
        
def plot(x,y):#平滑線を描く関数
    f = interp1d(x, y, kind='cubic')    # ３次スプライン補間
    xnew = np.linspace(20, 80, num=400)    # 関数fに使うxを生成
    
    #plt.xlim([0, 8])
    #plt.ylim([0, 14])
    plt.plot(x, y, 'o')
    plt.plot(xnew, f(xnew), '-')    # f(x)みたいな形で使える

if __name__ == '__main__':
    start_time = time.time()#処理開始時刻を記録
    data = np.zeros(13)
    
    """
    各層のフレーム数
    1層目：80 ~ 140
    2層目：240 ~ 300
    ３層目：408 ~ 468
    ４層目：568 ~ 628
    5:736
    6:896
    7:1064
    8:1224
    9:1392
    10:1552
    以降328あげれば2層上がる
    
    """
    bottom = 240
    top = 300
    #分析層数
    start = 2
    n = 1
    step = 1
    y_all = np.array([0,0])
    for layer in range(start,start+n,step):
    """
    #偶数層と奇数層の判別、frameに開始frameを入力
    print(str(layer) + "層目")
    if layer%2 == 0:#偶数層
        print("偶数層")
        frame = int(240 + (int(layer/2)-1)*328)
    else:#奇数層
        print("奇数層")
        frame = int(80 + (int(layer-1)/2)*328)
    """
    
    for i in range(frame,frame+61):
        data = np.append(data,meltpool_width(i))
    
    data = data[13:]
    y=data
    data_ave = np.sum(data)/np.sum(np.where(data > np.mean(data), 1, 0))
    print(data_ave)
    y_all = np.append(y_all, data_ave)
    if layer == 1:
        y1 = data
    else:
        y2 = data
    x = np.arange(frame, frame+61)
    #x = np.arange(61)
    data = np.zeros(13)
    #plt.plot(x, y, 'o')
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(x, y, marker="o", color = "red")
    plt.title("layer" + str(layer))
    x_all = np.arange(start,start+n,step)
    y_all = y_all[2:]
    #plt.plot(x_all, y_all, 'o')
    
    
    
    # 1行2列に分割した中の1(左側)
    
    # 1行2列に分割した中の2(右側)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(x_all, y_all, marker="o", color = "blue")
    #plt.title("relation of layer and melt pool size")
    
    
    #処理終了
    #処理時間の計算と表示
    elapsed_time = time.time() - start_time
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    
    