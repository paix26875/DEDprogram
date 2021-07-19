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



if __name__ == '__main__':
    print('laser power? 1400 / 1600 / 1800')
    laser_power = int(input())
    print('after / before projection?')
    afbf = input()
    if afbf == "after":
        height = 90
        width = 120
    else:
        height = 500
        width = 600
    
    print('Average range')
    average = int(input())
    path = "/Users/paix/Desktop/Python_lab/frame_data/20210421/CMOS/" + afbf + "_projection/" + str(laser_power)
    path = "/Users/paix/Desktop/Python_lab/frame_data/20210519/17-2/"
    files = os.listdir(path)
    count = len(files)  
    # ic(count)
    threshold = 20
    dir_name = '/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/src/' + str(laser_power) + '/' + afbf + '/'
    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210519/temp/17-2/"
    ic(len(os.listdir(dir_name)))
    if len(os.listdir(dir_name)) != count:
        for i in range(0,count):
            ic(i)
            img_CMOS = np.array(Image.open(path + '/img_' + str(i) + '.bmp'))
            # img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/dstName.bmp'))
            # x,y = gp.get_gravitypoint_CMOS(img_CMOS,  show_gp_img = False)
            # trimmed_img_r = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 0]
            # trimmed_img_g = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 1]
            # trimmed_img_b = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 2]
            trimmed_img_r = img_CMOS[ 300 : 800 , 0 : 600, 0]
            trimmed_img_g = img_CMOS[ 300 : 800 , 0 : 600, 1]
            trimmed_img_b = img_CMOS[ 300 : 800 , 0 : 600, 2]
            
            img_zero = np.zeros(height*width)
            
            img_red = trimmed_img_r[:,:].reshape(height*width)
            ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
            trimmed_img_r = trimmed_img_r.reshape(height*width)
            trimmed_img_g = trimmed_img_g.reshape(height*width)
            trimmed_img_b = trimmed_img_b.reshape(height*width)
            for j in img_thresh.nonzero():
                if average == 50:
                    img_zero[j] += trimmed_img_r[j]*12.08469623 + trimmed_img_g[j]*0.38873001 + trimmed_img_b[j]*6.39120529 + 649.11480838
                    # R2 = 0.9396009510337889
                elif average == 30:
                    img_zero[j] += trimmed_img_r[j]*33.1964025 + trimmed_img_g[j]*(-7.2232028) + trimmed_img_b[j]*(-4.91897297) + 814.99889006
                elif average == 40:
                    img_zero[j] += trimmed_img_r[j]*14.34907861 + trimmed_img_g[j]*31.37619256 + trimmed_img_b[j]*(-25.21939576) + 928.53314193
                    # R2 = 0.9316342890510434
                elif average == 10:
                    img_zero[j] += trimmed_img_r[j]*20.76836881 + trimmed_img_g[j]*5.96208386 + trimmed_img_b[j]*(-13.79605271) + 1451.05263058
                    # R2 = 0.46292409520051325
                elif average == 20:
                    img_zero[j] += trimmed_img_r[j]*32.33573199 + trimmed_img_g[j]*5.89798715 + trimmed_img_b[j]*(-17.63821396) + 995.72135974
                    # R2 = 0.8781357329413082
                elif average == 0:
                    img_zero[j] += trimmed_img_r[j]*4.38956737 + trimmed_img_g[j]*0.90104765 + trimmed_img_b[j]*(-1.66704229) + 1871.91955832
            # ic(img_zero)
            # twocolor_CMOS = tc.tocolor(img_zero).reshape(height, width, 3)
            twocolor_CMOS = tc.tocolor(img_zero, height, width).reshape(height, width, 3)
            # ic(twocolor_CMOS)
            img_ave = np.array(twocolor_CMOS, dtype=np.int8)
            pil_img = Image.fromarray(img_ave, mode="RGB")
            save_name = str(i) + "_RGB.bmp"
            # pil_img.save('calibration/time_average/colorimg/CMOS_int8_RGBmin' + str(threshold) + save_name)
            pil_img.save(dir_name + 'img_' + str(average) + afbf + str(threshold) + save_name)
    else:
        import glob

        img_array = []
        # for filename in sorted(glob.glob(dir_name + "*.BMP")):
        ic(count)
        for filenum in range(0, count):
            save_name = str(filenum) + "_RGB.bmp"
            filename = dir_name + "img_"  + str(average) + afbf + str(threshold) + save_name
            # print(filename)
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        name = '/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/src/' + str(laser_power) + '/' + afbf + 'CMOS_meltpool.mp4'
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MP4V'), 15.0, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()

