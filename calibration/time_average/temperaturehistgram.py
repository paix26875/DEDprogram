import cv2
from PIL import Image
import numpy as np
from icecream import ic
import gravitypoint as gp
import trimming as tr
import twocolor_convert as tc
from matplotlib import pyplot as plt
import os


# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)

if __name__ == '__main__':

    # レーザ出力とフレーム数の設定
    # pathの設定
    print("ヒストグラム表示したい画像のパスを入力")
    color_img_path = input()
    if os.path.exists(color_img_path):
    # if False:
        img_pil = Image.open(color_img_path)
        img_np = np.array(img_pil)
        h, w = img_np[:,:,0].shape
        ic(h)
        ic(w)
        temperature_ave = tc.totemperature(img_np)
        TEMP = temperature_ave# 1次元配列
        TEMPplt = temperature_ave.reshape(h*w)# 2次元配列
        # # 温度ヒストグラム表示
        plt.hist(TEMPplt, color="red", bins=128)
        # plt.ylim(0, 200)
        plt.ylim(0, 2500)
        plt.xlim(1300, 3000)
        plt.xlabel("temperature")
        plt.show()