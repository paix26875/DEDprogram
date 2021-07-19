from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from imgIndexMeltpool import countFile
from imgIndexMeltpool import imgIndex
from icecream import ic

def toColor(filename):
    img = np.asarray(Image.open(filename).convert("RGB")).reshape(-1,3)
    red = img[0:, 0]
    green = img[0:, 1]
    blue = img[0:, 2]
    return red, green, blue

def pltHistgram(blue):
    # plt.hist(img, color=["red", "green", "blue"], bins=128)
    # plt.hist(red, color=["red"], bins=128)
    # plt.hist(green, color=["green"], bins=128)
    plt.hist(blue, color=["red"], bins=128)
    plt.ylim(0, 200)
    plt.xlim(1300, 3000)
    plt.show()

def color_hist(filename):
    img = np.asarray(Image.open(filename).convert("RGB")).reshape(-1,3)
    red = img[0:, 0]
    green = img[0:, 1]
    blue = img[0:, 2]
    # plt.hist(img, color=["red", "green", "blue"], bins=128)
    plt.hist(red, color=["red"], bins=128)
    plt.hist(green, color=["green"], bins=128)
    plt.hist(blue, color=["blue"], bins=128)
    plt.ylim(0, 50)
    plt.xlim(0, 260)
    plt.show()

if __name__ == "__main__":
    O_TEMP_Y=200
    O_TEMP_X=280
    O_USB_Y=193
    O_USB_X=267
    height=70
    width=60
    temp = 1400
    TEMP = np.reshape(np.zeros(height*width),(height,width))# 温度情報格納用の配列
    temp_b = [160, 10, 188, 248, 144, 40, 207, 239, 118, 71, 222, 255]# 色情報と温度情報の対応付け
    temp_base = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/"# 二色温度計画像の絶対パス
    temp_src = ["1400-181-3908.BMP", "1600-164-3805.BMP", "1800-177-3813.BMP"]# 二色温度計画像のファイル名
    # img_temp_all = Image.open('C:/Users/paix/Documents/Thermera/キャリブレーション用データ/1800W_141_2835/全温度.bmp')9
    for LaserPower in temp_src:
        img_temp_all = Image.open(temp_base + LaserPower)
        img_temp_np = np.array(img_temp_all)#画素値numpy化
        img_temp_b=img_temp_np[O_TEMP_Y:O_TEMP_Y+height, O_TEMP_X:O_TEMP_X+width,2]#90×90の配列にする                      
        
        # 色情報を温度情報に変換
        for i in range(12):
            img_temp_single=np.where(img_temp_b == temp_b[i],temp,0)#
            TEMP += img_temp_single
            temp += 100
        # ヒストグラム表示
        y = TEMP.reshape(4200,)
        pltHistgram(y)

        # 要素数カウント
        length = y[y.nonzero()]
        ic(length.size)

        # 数値リセット
        temp = 1400
        TEMP = np.reshape(np.zeros(height*width),(height,width))
    # color_hist("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp")
    color_hist("/Users/paix/Desktop/Python_lab/dstName.bmp")
    # color_hist("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/1600/img_164.bmp")
    # sumred = np.zeros(1600000)
    # sumgreen = ([])
    # sumblue = ([])
    # dirname = "/Users/paix/Desktop/Python_lab/frame_data/20201123/84-1800"
    # filenum = countFile(dirname)
    # framenum = np.sum(imgIndex(dirname))
    # for i in range(1,filenum):
    #     filename = dirname + "/img_" + str(i) + ".bmp"
    #     red, green, blue = toColor(filename)
    #     print(red)
    #     sumred += red
    # print(sumred)
    # avered = sumred / framenum
    # pltHistgram(avered)








# color_hist("frame_data/20201123/83-2000-2/img_48.bmp"
# )
# color_hist("frame_data/20201123/84-1200/img_53.bmp")
# color_hist("frame_data/20201123/84-1200/img_139.bmp")

# color_hist("frame_data/20201123/84-1800/img_120.bmp")
# color_hist("/Users/paix/Desktop/Python_lab/frame_data/20201123/84-1800/img_53.bmp")

# color_hist("frame_data/20201123/84-1800/img_116.bmp")

# color_hist("frame_data/20201123/85-1200/img_0.bmp")