"""
色情報を温度配列に
温度配列
を色情報に変換する
"""
from PIL import Image
import cv2
import numpy as np
from icecream import ic
import gravitypoint as gp
import trimming as tr

def tocolor(temperature_np):
    """
    二色温度計画像の温度配列を色画像に変換

    Parameters
    ----------
    temperature_np : numpy
        二色温度計の温度情報が入った配列
    
    Returns
    -------
    img_color : numpy
        二色温度計の色画像が入った配列
    """
    # 色と温度の対応データの読み込み
    csv_path = "/Users/paix/Desktop/Python_lab/colortotemperature/color_to_temperature.csv"
    csv_data = np.loadtxt(csv_path, delimiter=',')
    TEMPERATURE = csv_data[:, :1]
    # ic(TEMPERATURE)
    # RGB = np.array(csv_data[:, 1:4], dtype=np.int8)
    RGB = csv_data[:, 1:4]
    temperature_np = temperature_np.reshape(temperature_np.size)
    ic(temperature_np.size)
    img_zero = np.array([0,0,0])
    img_color = np.array([0,0,0])
    # ic(img_zero.shape)

    for temp in temperature_np:
        ii = 0
        temp = int(round(temp, -1))
        # ic(temp)
        if temp < 1310 or temp > 2600:
            img_color = np.concatenate([img_color, img_zero])
            continue
        elif temp == 0:
            img_color = np.concatenate([img_color, img_zero])
            continue
        else:
            for TEMP in TEMPERATURE:
                ii += 1
                if temp == TEMP:
                    # print("hey")
                    # ic(img_color.shape)
                    # ic(RGB[ii-1].shape)
                    img_color = np.concatenate([img_color, RGB[ii-1]])
    img_color = img_color[3: ]
    img_color = img_color.reshape(90, 120, 3)

    return img_color

    pass


def totemperature(img_color):
    """
    二色温度計画像の色画像を温度配列に変換

    Parameters
    ----------
    img_color : numpy
        二色温度計の色画像が入った配列
    
    Returns
    -------
    temperature_np : numpy
        二色温度計の温度情報が入った配列
    """
    # 色と温度の対応データの読み込み
    csv_path = "/Users/paix/Desktop/Python_lab/colortotemperature/color_to_temperature.csv"
    csv_data = np.loadtxt(csv_path, delimiter=',')
    TEMPERATURE = csv_data[:, :1]
    # ic(TEMPERATURE)
    # RGB = np.array(csv_data[:, 1:4], dtype=np.int8)
    RGB = csv_data[:, 1:4]
    # 小数点があるとエラーになるので8ビットの整数型に変換
    # img_color = np.array(img_color, dtype=np.uint8)
    img_color = np.array(img_color)

    # 温度データ格納用の配列を用意
    img_zero = np.zeros(img_color.shape)
    temperature_np = np.squeeze(np.delete(img_zero, np.s_[1:], 2))
    
    height, width = img_color[:,:,0].shape
    img_r = img_color[:,:,0].reshape(height*width)
    img_g = img_color[:,:,1].reshape(height*width)
    img_b = img_color[:,:,2].reshape(height*width)
    temperature_np = temperature_np.reshape(height*width)
    ic(img_r.size)
    for i in range(img_r.size):
        ii = 0
        if img_r[i] == 0 and img_g[i] == 0 and img_b[i] == 0:
            continue
        for rgb in RGB:
            ii += 1
            if img_r[i] == int(rgb[0]) and img_g[i] == int(rgb[1]) and img_b[i] == int(rgb[2]):
                temperature_np[i] = TEMPERATURE[ii-1]
    temperature_np = temperature_np.reshape(height, width)
    return temperature_np

if __name__ == '__main__':
    # img = np.array(Image.open("/Users/paix/Desktop/Python_lab/calibration/time_average/img_ave_save_pillow.bmp"))
    img = np.array(Image.open("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolors/1600_600/16000OUT3805.BMP"))

    # トリミング処理
    rough_trimmed_img = tr.img_trimming(img, 220, 310, 640, 1279)
    x, y = gp.get_gravitypoint_img(rough_trimmed_img)# うまくいった
    trimmed_img = rough_trimmed_img[ : , x - 60 : x + 60]
    gp.get_gravitypoint_img(trimmed_img)

    # # 画像保存
    # img_ave = np.array(trimmed_img, dtype=np.int8)
    # pil_img = Image.fromarray(img_ave, mode="RGB")
    # pil_img.save('calibration/time_average/img_ave_save_pillow.bmp')

    # temperature_np = totemperature(trimmed_img)
    # img_color = tocolor(temperature_np)

    # # 画像保存
    # img_ave = np.array(img_color, dtype=np.int8)
    # pil_img = Image.fromarray(img_ave, mode="RGB")
    # pil_img.save('calibration/time_average/img_ave_save_pillow.bmp')
    