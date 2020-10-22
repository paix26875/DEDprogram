# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:03:21 2020

@author: paix
"""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Ｒのデータ分布算出
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""
処理時間計測
"""""""""""""""
#-*- using:utf-8 -*-
import time
import sys, time
# sys.path.append('/Users/paix/Desktop/Python/Automatic_Detection.py')
import numpy as np
import csv
from matplotlib import pyplot as plt
from PIL import Image
from scipy.interpolate import interp1d
from Automatic_Detection import auto_detection
from Automatic_Detection import RGBvalue

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
    start = time.time()#処理開始時刻を記録
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
    bottom = 1000
    top = bottom + 50
    n = 0
    for i in range(bottom,top):
        data += RGBvalue(i)
        #print(RGBvalue(i))
        if np.all(RGBvalue(i)) != 0:
            n += 1
    """
    データ分析
    """
    print("溶融池が映っている画像枚数：" + str(n))
    #グラフ描画パラメータ
    x=np.arange(20,85,5)
    #x=np.arange(1300,1950,50)
    """
    if n != 0:
        y=data/n
    else:
        y=data
    """
    y=data/np.sum(data)
    # array_info(x)
    # array_info(y)
    y_all=data/44
    plot(x, y)#プロットと平滑線を描画
    

    # plt.plot(x, y)
    # # [<matplotlib.lines.Line2D object at 0x121ca3be0>]
    plt.show()
    #処理終了
    #処理時間の計算と表示
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
