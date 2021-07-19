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
import time

def convertTtoC(temp):
    """
    温度値をRGBのカラーマップに変換する
    Parameters
    -----------
    temp : float
        温度
    
    Returns
    -----------
    RGB : numpy
        カラーマップ
    """
    RGB = np.array([])
    formula_increase = -0.0051 * temp^2 + 19.531 * temp - 18420
    if temp < 1685:
        RGB[0] = 0
    elif temp > 1875:
        RGB[0] = 255
    else:
        RGB[0] = formula_increase
        # R2 = 0.9996
    formula_increase = -0.0051 * temp^2 + 17.701 * temp - 15000
    formula_decrease = -0.0041 * temp^2 + 10.16 * temp - 5945.1
    if temp < 1490:
        RGB[2] = -0.0041 * temp^2 + 10.16 * temp - 5945.1
    elif 1490 <= temp < 1680:
        RGB[2] = -0.0051 * temp^2 + 17.701 * temp - 15000
    elif 1680:
        pass




def tocolor(temperature_np, height=90, width=120):
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
    # ic(temperature_np.size)
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
            if temp < 1690:
                img_color = np.append(img_color, 0)
                img_color = np.concatenate([img_color, RGB[(TEMPERATURE == temp).reshape(259),1:3].reshape(2)])
            elif temp > 1880:
                img_color = np.append(img_color, 255)
                img_color = np.concatenate([img_color, RGB[(TEMPERATURE == temp).reshape(259),1:3].reshape(2)])
            else:
                # ic((TEMPERATURE == temp).reshape(259))
            # ic(RGB[(TEMPERATURE == temp).reshape(259),0:3].reshape(3).shape)
            # ic(img_color.shape)
                img_color = np.concatenate([img_color, RGB[(TEMPERATURE == temp).reshape(259),0:3].reshape(3)])
            # for TEMP in TEMPERATURE:
            #     ii += 1
            #     if temp == TEMP:
            #         # print("hey")
            #         # ic(img_color.shape)
            #         # ic(RGB[ii-1].shape)
            #         img_color = np.concatenate([img_color, RGB[ii-1]])
    

    img_color = img_color[3: ]
    # img_color = img_color.reshape(300, 300, 3)
    img_color = img_color.reshape(height, width, 3)

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
    # temperature_np = temperature_np.reshape(height*width)
    temperature_np = temperature_np.reshape(-1)
    # ic(img_r.size)
    # for i in range(img_r.size):
    # size = np.array(img_r.nonzero()).shape[1]
    # ic(np.array(img_r.nonzero()).shape[1])
    for i in np.array(img_r.nonzero()).reshape(-1):
        ii = 0
        if img_r[i] == 0 and img_g[i] == 0 and img_b[i] == 0:
            continue
        elif img_r[i] == 0:
            for rgb in RGB[:77]:
                ii += 1
                if img_r[i] == int(rgb[0]) and img_g[i] == int(rgb[1]) and img_b[i] == int(rgb[2]):
                    temperature_np[i] = TEMPERATURE[ii-1]
                    break
        elif img_r[i] < 255:
            ii=75
            for rgb in RGB[76:115]:
                ii += 1
                if img_r[i] == int(rgb[0]) and img_g[i] == int(rgb[1]) and img_b[i] == int(rgb[2]):
                    temperature_np[i] = TEMPERATURE[ii-1]
                    break
        else:
            ii=113
            for rgb in RGB[114:]:
                ii += 1
                if img_r[i] == int(rgb[0]) and img_g[i] == int(rgb[1]) and img_b[i] == int(rgb[2]):
                    # ic(temperature_np.shape)
                    temperature_np[i] = TEMPERATURE[ii-1]
                    break
    temperature_np = temperature_np.reshape(height, width)
    return temperature_np

if __name__ == '__main__':
    # img = np.array(Image.open("/Users/paix/Desktop/Python_lab/calibration/time_average/img_ave_save_pillow.bmp"))
    img = np.array(Image.open("/Users/paix/Desktop/Python_lab/frame_data/20210610/temperature/1600_1000_11/img_24.bmp"))

    # # トリミング処理
    # rough_trimmed_img = tr.img_trimming(img, 220, 310, 640, 1279)
    # x, y = gp.get_gravitypoint_img(rough_trimmed_img)# うまくいった
    # trimmed_img = rough_trimmed_img[ : , x - 60 : x + 60]
    # gp.get_gravitypoint_img(trimmed_img)

    # # 画像保存
    # img_ave = np.array(trimmed_img, dtype=np.int8)
    # pil_img = Image.fromarray(img_ave, mode="RGB")
    # pil_img.save('calibration/time_average/img_ave_save_pillow.bmp')
    start = time.time()

    temperature_np = totemperature(img)

    end = time.time()

    ic(temperature_np)
    ic(end - start)

    start = time.time()
    
    img_color = tocolor(temperature_np, 300, 300)

    end = time.time()
    ic(end - start)
    # # 画像保存
    img_ave = np.array(img_color, dtype=np.int8)
    pil_img = Image.fromarray(img_ave, mode="RGB")
    pil_img.save('/Users/paix/Desktop/Python_lab/frame_data/20210610/temperature/RGB.bmp')
    