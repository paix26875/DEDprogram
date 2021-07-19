from PIL import Image
import numpy as np
import gravitypoint as gp
import twocolor_convert as tc
from icecream import ic
# import cv2
import os
import time
from matplotlib import pyplot as plt
import glob


if __name__ == '__main__':

    print('which type? laser / feed / EFconstant')
    type = input()
    laser_list = ['1000', '1200', '1400', '1600', '1800', '2000']
    feed_list = ['625', '750', '875', '1000', '1125', '1250']
    EFconstant_list = ['1000-625', '1200-750', '1400-875', '1600-1000', '1800-1125', '2000-1250']
    fname = '/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/' + type + '_temperature_histgram.csv'
    all_hist = np.loadtxt(fname, delimiter=',')
    all_hist = np.flipud(all_hist) # 上下を反転（matplotlibの仕様上左上が原点になってしまうため）
    h, w = all_hist.shape

    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

    fig = plt.figure(num=None, dpi=80,figsize=(9, 7)) 
    ax = fig.add_subplot(111) 
    #fig, ax = plt.subplots() 
    plt.imshow(all_hist, cmap='jet') 
    plt.colorbar(label='ピクセル数 [px]')
    
    if type == 'laser':
        plt.xticks(np.arange(w), laser_list)
        ax.set_xlabel("レーザ出力 [W]")
        ax.set_ylabel("溶融地温度 [℃]")
        title = "レーザ出力と溶融地温度の関係"

    elif type == 'feed':
        plt.xticks(np.arange(w), feed_list)
        ax.set_xlabel("レーザ走査速度 [mm/min]")
        ax.set_ylabel("溶融地温度 [℃]")
        title = "レーザ走査速度と溶融地温度の関係"

    elif type == 'EFconstant':
        plt.xticks(np.arange(w), EFconstant_list)
        ax.set_xlabel("レーザ出力 [W]/レーザ走査速度 [mm/min]")
        ax.set_ylabel("溶融地温度 [℃]")
        title = "入力エネルギ密度一定の時の溶融地温度"
    
    fig.text(0.30, 0.02, title, fontsize=14)
    ylabel = np.array(np.arange(2500, 1500, -20), dtype=object)
    plt.yticks(np.arange(h), ylabel) 
    ax.set_aspect(w/h) 
    plt.show()

    os.makedirs('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/2Dhistgram/', exist_ok=True)
    fig.savefig('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/2Dhistgram/' + type + '_temperature_histgram.png')