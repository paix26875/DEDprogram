# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:23:24 2020

@author: paix
"""

"""
自動検出機能作成
"""
import time
import sys, time
import numpy as np
import csv
from matplotlib import pyplot as plt
from PIL import Image
from scipy.interpolate import interp1d

def array_info(x):
    print("配列のshape", x.shape)
    print("配列の要素のデータ型", x.dtype)
    print("配列の中身\n",x,"\n")
    
def plot(x,y):
    """
    pyplot.plot(x,y,label='layer')#第３引数はラベル
    #pyplot.title(str(FEEDRATE)+'%')#グラフタイトル
    pyplot.xlabel('R')#ｘ軸ラベル
    pyplot.ylabel('pixel')#ｙ軸ラベル
    pyplot.legend()#凡例表示
    pyplot.show#グラフ描画
    """
    f = interp1d(x, y, kind='cubic')    # ３次スプライン補間
    xnew = np.linspace(20, 80, num=400)    # 関数fに使うxを生成
    
    #plt.xlim([0, 8])
    #plt.ylim([0, 14])
    plt.plot(x, y, 'o')
    plt.plot(xnew, f(xnew), '-')    # f(x)みたいな形で使える
    
def detection_r20(img_all):   
    w,h = img_all.size
    img_all_np = np.array(img_all)
    img = img_all_np[:, :, 2]#画像のR値のみ抜き出し
    #for i in range

"""
自動で溶融池を検出
自動でトリミング
"""
def auto_detection(img_all, co_num):
    w, h= img_all.size
    #print(w)
    #print(h)
    img_all_np = np.array(img_all)#画素値numpy化
    img_r = img_all_np[:, :, 2]#画像のR値のみ抜き出し
    img_rh = img_r[:,int(w/2)]#w/2のR値取得
    if np.all(img_rh < 20) == True:
        return 0
    else:
        rh0=0
        rh1=0
        for i in range(h):
            if img_rh[i] > 20:
                rh0 = i
                break
        for i in range(h-1,0,-1):
            if img_rh[i] > 20:
                rh1 = i
                break
        #print(rh0)#溶融池上端
        #print(rh1)#溶融池下端
        r0 = int((rh0 + rh1)/2)#溶融池中心座標
        img_rw = img_r[r0, :]
        rw0=0
        rw1=0
        
        for i in range(r0):
            if img_rw[i] > 20:
                rw0 = i
                break
        for i in range(w-1, r0, -1):
            if img_rw[i] > 20:
                rw1 = i
                break
        #print(rw0)#溶融池左端
        #print(rw1)#溶融池右端
        rw = int(rw1 - rw0)#溶融池幅
        rh = int(rh1 - rh0)#溶融池高さ
        
        start_x = int(rw0 - rw*0.3)#分析開始点
        start_y = int(rh0 - rh*0.3)#分析開始点
        mp_w = int(rw*1.6)#分析幅
        mp_h = int(rh*1.6)#分析高さ
        if co_num==0:
            return_img = img_r[start_y:start_y + mp_h, start_x:start_x + mp_w]
        else:
            return_img = img_r[start_y:start_y + mp_h, start_x:start_x + mp_w]
            return_img = np.reshape(return_img, (mp_w*mp_h,))
        #print("溶融池幅：" + str(mp_w))
        #print("溶融池高さ：" + str(mp_h))
        #print("分析ピクセル数：" + str(mp_h*mp_w))
        return return_img

def meltpool_width(frame):
    #処理開始
    img_all = Image.open('data/temp/2020_0202/result_150/sample_video_img_' + str(frame) + '.bmp')
    #sum_r = np.zeros(13)
    print("フレーム数：" + str(frame))
    img_r = auto_detection(img_all,0)#自動検出機能
    if np.all(img_r) == 0:
        return 0
    else:
        img_r = np.where(img_r > 20, 1, 0)
        img_r = np.sum(img_r, axis=1)
        melt_width = np.amax(img_r)
        return melt_width
    
def meltpool_size(frame):
    #処理開始
    img_all = Image.open('data/temp/2020_0202/result_150/sample_video_img_' + str(frame) + '.bmp')
    #sum_r = np.zeros(13)
    print("フレーム数：" + str(frame))
    img_r = auto_detection(img_all,0)#自動検出機能
    if np.all(img_r) == 0:
        return 0
    else:
        img_r = np.where(img_r > 20, 1, 0)
        img_r = np.sum(img_r)
        melt_size = img_r
        return melt_size
        

def RGBvalue(frame):
    #処理開始
    img_all = Image.open('data/temp/2020_0202/result_150/sample_video_img_' + str(frame) + '.bmp')
    #sum_r = np.zeros(13)
    data = np.zeros(60)
    print("フレーム数：" + str(frame))
    img_r = auto_detection(img_all,1)#自動検出機能
    if np.all(img_r) == 0:
        return 0
    else:
        
        """
        RGB解析
        """
        for i in range(0,img_r.size):
        #for i in (0,img_r.size-1):
            data[(int(img_r[i])+2)//5-4] +=1
            #print((int(img_r[i])+2)//5-4)
            #print(i)
        #print(data[:13])
        data = data[:13]
        """
        #sum_r[(img_r[i]+2)//2]
        for i in range(20,85,5):
            r = len([n for n in img_r if i-3<n<i+3])
            sum_r = np.append(sum_r,r)
            #print(r)
            
        
        sum_r = sum_r[13:]
        """
        #print("解析")
        return data
    
    
    
if __name__ == '__main__':
    frame = 6362
    #frame = 260
    img_all = Image.open('data/temp/2020_0202/result_150/sample_video_img_' + str(frame) + '.bmp')
    img_r = auto_detection(img_all,0)#自動検出機能    
    print(img_r)
    """
    img_tol = auto_detection(img_all,0)#自動検出機能
    img_two = np.where(img_tol > 20, 1, 0)
    img_sum = np.sum(img_two, axis=1)
    img_max = np.amax(img_sum)
    """
    
    
    
    
    