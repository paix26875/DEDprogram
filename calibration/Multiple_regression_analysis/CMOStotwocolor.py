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
    print('laser power? 1400 / 1600 / 1800')
    laser_power = int(input())
    height = 300
    width = 300
    print('after / before projection?')
    afbf = input()
    print('Average range')
    average = int(input())
    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210421/CMOS/" + afbf + "_projection/"
    if laser_power == 1400:
        img_CMOS = np.array(Image.open(dir_name + '1400/img_72.bmp'))
    elif laser_power == 1600:
        img_CMOS = np.array(Image.open(dir_name + '1600/img_86.bmp'))
    elif laser_power == 1800:
        img_CMOS = np.array(Image.open(dir_name + '1800/img_95.bmp'))
    # img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/dstName.bmp'))
    x,y = gp.get_gravitypoint_CMOS(img_CMOS)
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
    for i in img_thresh.nonzero():
        if average == 50:
            img_zero[i] += trimmed_img_r[i]*12.08469623 + trimmed_img_g[i]*0.38873001 + trimmed_img_b[i]*6.39120529 + 649.11480838
            # R2 = 0.9396009510337889
        elif average == 30:
            img_zero[i] += trimmed_img_r[i]*33.1964025 + trimmed_img_g[i]*(-7.2232028) + trimmed_img_b[i]*(-4.91897297) + 814.99889006
        elif average == 40:
            img_zero[i] += trimmed_img_r[i]*14.34907861 + trimmed_img_g[i]*31.37619256 + trimmed_img_b[i]*(-25.21939576) + 928.53314193
            # R2 = 0.9316342890510434
        elif average == 10:
            img_zero[i] += trimmed_img_r[i]*20.76836881 + trimmed_img_g[i]*5.96208386 + trimmed_img_b[i]*(-13.79605271) + 1451.05263058
            # R2 = 0.46292409520051325
        elif average == 20:
            img_zero[i] += trimmed_img_r[i]*32.33573199 + trimmed_img_g[i]*5.89798715 + trimmed_img_b[i]*(-17.63821396) + 995.72135974
            # R2 = 0.8781357329413082
        elif average == 0:
            img_zero[i] += trimmed_img_r[i]*4.38956737 + trimmed_img_g[i]*0.90104765 + trimmed_img_b[i]*(-1.66704229) + 1871.91955832
    ic(img_zero)
    # twocolor_CMOS = tc.tocolor(img_zero).reshape(height, width, 3)
    twocolor_CMOS = tc.tocolor(img_zero, height, width).reshape(height, width, 3)
    ic(twocolor_CMOS)
    img_ave = np.array(twocolor_CMOS, dtype=np.int8)
    pil_img = Image.fromarray(img_ave, mode="RGB")
    save_name = str(laser_power) + "_RGB.bmp"
    # pil_img.save('calibration/time_average/colorimg/CMOS_int8_RGBmin' + str(threshold) + save_name)
    # pil_img.save('/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/temp/CMOS_raw_int8_RGBmin' + str(average) + afbf + str(threshold) + save_name)



    # RGBvalue = 1
    # CMOS = trimmed_img[:, :, RGBvalue]
    # height = 90
    # width = 120
    # RGBmin = 20
    # RGBmax = 255