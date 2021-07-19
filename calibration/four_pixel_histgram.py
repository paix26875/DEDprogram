from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from imgIndexMeltpool import countFile
from imgIndexMeltpool import imgIndex
from icecream import ic

if __name__ == '__main__':
    filename = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp"
    img = np.asarray(Image.open(filename).convert("RGB"))
    O_TEMP_Y=200
    O_TEMP_X=280
    O_USB_Y=193
    O_USB_X=267
    height=70
    width=60

    # red = img[0:, 0:, 0]
    red = img[O_USB_Y:O_USB_Y+height, O_USB_X:O_USB_X+width, 0]#90×90の配列にするかつRを抜き出す（第3引数）
    green = img[0:, 0:, 1]
    blue = img[0:, 0:, 2]

    # height = img.shape[0]
    # width = img.shape[1]

    x = np.zeros(13)

    ic(red.shape)
    for i in range(height-1):
        for j in range(width-1):
            if red[i,j]:
                # CMOS_ave = (img[i,j, RGB] + img[i,j+1, RGB] + img[i+1,j, RGB] + img[i+1,j+1, RGB])/4
                CMOS_ave = (int(red[i,j]) + int(red[i,j+1]) + int(red[i+1,j]) + int(red[i+1,j+1]))/4
                x = np.append(x,CMOS_ave)
            else:
                x = np.append(x,0)
    x = x[13:]
    # red = img[0:, 0]
    # green = img[0:, 1]
    # blue = img[0:, 2]
    # plt.hist(img, color=["red", "green", "blue"], bins=128)
    # plt.hist(red, color=["red"], bins=128)
    # plt.hist(green, color=["green"], bins=128)
    # plt.hist(blue, color=["blue"], bins=128)
    plt.hist(x, color=["red"], bins=128)
    plt.ylim(0, 50)
    plt.xlim(0, 260)
    plt.show()