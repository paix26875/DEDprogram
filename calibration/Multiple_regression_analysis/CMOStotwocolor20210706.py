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
    print('laser power? 1400 / 1500 / 1600 / 1700 / 1800')
    laser_power = int(input())
    height = 300
    width = 300
    # print('after / before projection?')
    # afbf = input()
    print('Average range')
    average = int(input())
    print('Gain? 16 / 24')
    gain = int(input())
    print('nonzero? nonzero / haszero')
    nonzero = input()
    for laser_power in range(1400,1900,100):
        for gain in[16,24]:
            for average in range(10,60,10):
                for nonzero in['nonzero', 'haszero']:
                    if gain == 16:
                        dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g16/"
                        mid_frames = [28, 41, 31, 39, 36]
                    elif gain == 24:
                        dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g24/"
                        mid_frames = [32, 38, 32, 26, 57]
                    mid_frame = mid_frames[int((laser_power-1400)/100)]
                    img_CMOS = np.array(Image.open(dir_name + str(laser_power) + '/img_' + str(mid_frame) + '.bmp'))
                    
                    x,y = gp.get_gravitypoint_CMOS(img_CMOS, show_gp_img = False)
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
                        if gain == 16:
                            if average == 10:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(6.537611491206067) + trimmed_img_g[i]*(3.4013504316366463) + trimmed_img_b[i]*(4.095604828599058) + 1577.58602285# 0を含まないcsvデータ
                                    # R2 = 0.9341891184851117
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*3.1522073664433723 + trimmed_img_g[i]*(-0.07828546412009807) + trimmed_img_b[i]*(12.771525414527204) + 1440.22687672# 0を含むcsvデータ
                                    # R2 = 0.9136344463509365
                            elif average == 20:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(6.529131025686352) + trimmed_img_g[i]*(0.6173487122400187) + trimmed_img_b[i]*(6.6331991509576325) + 1558.31558887# 0を含まないcsvデータ
                                    # R2 = 0.9891891850085146
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(4.0354719103857) + trimmed_img_g[i]*(1.4863775188739439) + trimmed_img_b[i]*(9.489171062603443) + 1496.51781306# 0を含むcsvデータ
                                    # R2 = 0.9632183488266568
                            elif average == 30:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(-0.6963221862605778) + trimmed_img_g[i]*(2.1393438003730765) + trimmed_img_b[i]*(11.345074017781336) + 1557.98769305# 0を含まないcsvデータ
                                    # R2 = 0.9922455663925057
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(3.5033905652963253) + trimmed_img_g[i]*(2.2893083378806676) + trimmed_img_b[i]*(10.348201394010237) + 1455.07007854# 0を含むcsvデータ
                                    # R2 = 0.9566073170963383
                            elif average == 40:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(4.4385086516917065) + trimmed_img_g[i]*(-0.914144582729036) + trimmed_img_b[i]*(10.993850641179169) + 1499.49979127# 0を含まないcsvデータ
                                    # R2 = 0.9943362912333767
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(3.502617395154935) + trimmed_img_g[i]*(2.62906711905843) + trimmed_img_b[i]*(11.245621813344592) + 1409.10262974# 0を含むcsvデータ
                                    # R2 = 0.9533777599616395
                            elif average == 50:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(5.961674220316115) + trimmed_img_g[i]*(-0.8150562132893455) + trimmed_img_b[i]*(10.719013038105013) + 1459.88279036# 0を含まないcsvデータ
                                    # R2 = 0.9935012645732142
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(3.2142793661379776) + trimmed_img_g[i]*(2.7738922478349526) + trimmed_img_b[i]*(11.843752104958236) + 1392.14244718# 0を含むcsvデータ
                                    # R2 = 0.9557526612114268
                        elif gain == 24:
                            if average == 10:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*6.9811958 + trimmed_img_g[i]*0.1964151 + trimmed_img_b[i]*(3.83974463) + 1552.48784308 # 0を含まないcsvデータ
                                    # R2 = 0.9075940399134529
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*4.4788405 + trimmed_img_g[i]*2.09581999 + trimmed_img_b[i]*(4.3380916) + 1551.4651406 # 0を含むcsvデータ
                                    # R2 = 0.8993108929849997
                            elif average == 20:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(8.908073140930705) + trimmed_img_g[i]*(-6.88935916151523) + trimmed_img_b[i]*(8.753746054079386) + 1507.28397621 # 0を含まないcsvデータ
                                    # R2 = 0.9419532659322372
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(0.6641260001769099) + trimmed_img_g[i]*(3.701258704116375) + trimmed_img_b[i]*(5.126694565509716) + 1591.98316074 # 0を含むcsvデータ
                                    # R2 = 0.9359743446358514
                            elif average == 30:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(8.0569917461762) + trimmed_img_g[i]*(-17.62168321828612) + trimmed_img_b[i]*(17.914101911773113) + 1511.57113924 # 0を含まないcsvデータ
                                    # R2 = 0.9694715052259318
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(3.456442222202001) + trimmed_img_g[i]*(3.780008371646069) + trimmed_img_b[i]*(3.8825103423733403) + 1539.67168086 # 0を含むcsvデータ
                                    # R2 = 0.9562190099420442
                            elif average == 40:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(25.353837300735524) + trimmed_img_g[i]*(-23.60460418295967) + trimmed_img_b[i]*(13.145961076581646) + 1302.20595068 # 0を含まないcsvデータ
                                    # R2 = 0.9642690784656309
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(41.789044943511776) + trimmed_img_g[i]*(2.5527853224056223) + trimmed_img_b[i]*(-16.52407754529958) + 1083.83051295 # 0を含むcsvデータ
                                    # R2 = 0.947551589884032
                            elif average == 50:
                                if nonzero == 'nonzero':
                                    img_zero[i] += trimmed_img_r[i]*(41.91545399748533) + trimmed_img_g[i]*(-16.741254808432817) + trimmed_img_b[i]*(-1.5077411437411694) + 1105.76905428 # 0を含まないcsvデータ
                                    # R2 = 0.9682417600126562
                                elif nonzero == 'haszero':
                                    img_zero[i] += trimmed_img_r[i]*(55.487685006950414) + trimmed_img_g[i]*(3.0853904034376267) + trimmed_img_b[i]*(-24.527991908982145) + 922.35833948 # 0を含むcsvデータ
                                    # R2 = 0.9624052034513891
                    ic(img_zero)
                    # twocolor_CMOS = tc.tocolor(img_zero).reshape(height, width, 3)
                    twocolor_CMOS = tc.tocolor(img_zero, height, width).reshape(height, width, 3)
                    ic(twocolor_CMOS)
                    img_ave = np.array(twocolor_CMOS, dtype=np.int8)
                    pil_img = Image.fromarray(img_ave, mode="RGB")
                    save_name = str(laser_power) + '_' + str(gain) + '_' + str(average) + '_' + nonzero + "_RGB" + ".bmp"
                    pil_img.save(dir_name + save_name)
                    # pil_img.save('/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/temp/CMOS_raw_int8_RGBmin' + str(average) + afbf + str(threshold) + save_name)