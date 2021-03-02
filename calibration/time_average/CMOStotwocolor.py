"""
CMOSカメラ画像→温度配列→二色温度計画像
"""
from PIL import Image
import numpy as np
import gravitypoint as gp
import twocolor_convert as tc
from icecream import ic
import cv2



if __name__ == '__main__':
    laser_power = 1600
    RGBvalue = 2
    if RGBvalue == 0:
        RGB = "R"
    elif RGBvalue == 1:
        RGB = "G"
    elif RGBvalue == 2:
        RGB = "B"
    if laser_power == 1400:
        img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1400/img_181.bmp'))
    elif laser_power == 1600:
        img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp'))
        # img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/1600/img_164.bmp'))
    elif laser_power == 1800:
        img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1800/img_177.bmp'))
    # img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/dstName.bmp'))
    x,y = gp.get_gravitypoint_CMOS(img_CMOS)
    trimmed_img = img_CMOS[ y - 45 : y + 45 , x - 60 : x + 60, RGBvalue]
    
    img_zero = np.zeros(90*120)
    
    threshold = 40
    img_red = trimmed_img[:,:].reshape(90*120)
    ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
    trimmed_img = trimmed_img.reshape(90*120)
    for i in img_thresh.nonzero():
        if RGBvalue == 0:
            img_zero[i] += trimmed_img[i] * 5.08 + 1510.8
        elif RGBvalue == 1:
            img_zero[i] += trimmed_img[i] * 4.06 + 1536.9
        elif RGBvalue == 2:
            img_zero[i] += trimmed_img[i] * 3.33 + 1566.77
    ic(img_zero)
    twocolor_CMOS = tc.tocolor(img_zero).reshape(90, 120, 3)
    ic(twocolor_CMOS)
    img_ave = np.array(twocolor_CMOS, dtype=np.int8)
    pil_img = Image.fromarray(img_ave, mode="RGB")
    save_name = str(laser_power) + "_" + str(RGB) + ".bmp"
    pil_img.save('calibration/time_average/colorimg/CMOS_int8_' + save_name)



    # RGBvalue = 1
    # CMOS = trimmed_img[:, :, RGBvalue]
    # height = 90
    # width = 120
    # RGBmin = 20
    # RGBmax = 255