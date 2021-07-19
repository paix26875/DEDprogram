"""
CMOSカメラ画像→温度配列→二色温度計画像
"""
from PIL import Image
import numpy as np
import gravitypoint as gp
import twocolor_convert as tc
from icecream import ic
import cv2
import os
import time


if __name__ == '__main__':
    print('laser power? 1000 / 1200 / 1400 / 1600 / 1800 / 2000')
    laser_power = input()
    height = 300
    width = 300
    print('feed rate? 625 / 750 / 875 / 1000 / 1125 / 1250')
    feed_rate = input()
    print('layer number? 1 / 5 / 11')
    layer_number = input()
    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210610/" + laser_power + "_" + feed_rate + "_" + layer_number + "/"
    # dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210610/test/"
    files = os.listdir(dir_name)
    count = len(files) 
    for i in range(count):
        start = time.time()
        ic(i)
        img_CMOS = np.array(Image.open(dir_name + 'img_' + str(i) + '.bmp'))
        # print(img_CMOS)
        # img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/dstName.bmp'))
        x,y = gp.get_gravitypoint_CMOS(img_CMOS, False)
        trimmed_img_r = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 0]
        trimmed_img_g = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 1]
        trimmed_img_b = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 2]
        
        img_zero = np.zeros(height*width)
        
        threshold = 20
        img_red = trimmed_img_r[:,:].reshape(height*width)
        ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
        trimmed_img_r = trimmed_img_r.reshape(height*width)
        trimmed_img_g = trimmed_img_g.reshape(height*width)
        trimmed_img_b = trimmed_img_b.reshape(height*width)
        for j in img_thresh.nonzero():
            img_zero[j] += trimmed_img_r[j]*20.76836881 + trimmed_img_g[j]*5.96208386 + trimmed_img_b[j]*(-13.79605271) + 1451.05263058
            # R2 = 0.46292409520051325
        # ic(img_zero)
        # twocolor_CMOS = tc.tocolor(img_zero).reshape(height, width, 3)
        twocolor_CMOS = tc.tocolor(img_zero, height, width).reshape(height, width, 3)
        # ic(twocolor_CMOS)
        img_ave = np.array(twocolor_CMOS, dtype=np.int8)
        pil_img = Image.fromarray(img_ave, mode="RGB")
        save_name = 'img_' + str(i) + ".bmp"
        # pil_img.save('calibration/time_average/colorimg/CMOS_int8_RGBmin' + str(threshold) + save_name)
        save_path = "/Users/paix/Desktop/Python_lab/frame_data/20210610/temperature/" + laser_power + "_" + feed_rate + "_" + layer_number + "/"
        os.makedirs(save_path, exist_ok=True)
        pil_img.save(save_path + save_name)
        end = time.time()
        elapsed_time = round(end - start, 3)
        ic(elapsed_time)



    # RGBvalue = 1
    # CMOS = trimmed_img[:, :, RGBvalue]
    # height = 90
    # width = 120
    # RGBmin = 20
    # RGBmax = 255