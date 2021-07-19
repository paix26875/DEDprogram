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
    height = 300
    width = 300
    # print('laser power? 1000 / 1200 / 1400 / 1600 / 1800 / 2000')
    # laser_power = input()
    # print('feed rate? 625 / 750 / 875 / 1000 / 1125 / 1250')
    # feed_rate = input()
    # print('layer number? 1 / 5 / 11')
    # layer_number = input()
    for laser_power in ['1000', '1200', '1400', '1600', '1800', '2000']:
        for feed_rate in ['625', '750', '875', '1000', '1125', '1250']:
            for layer_number in ['1', '5', '11']:
                ic(laser_power)
                ic(feed_rate)
                ic(layer_number)
                dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210610/" + laser_power + "_" + feed_rate + "_" + layer_number + "/"
                if os.path.exists(dir_name):
                    files = os.listdir(dir_name)
                    count = len(files)
                    save_path = "/Users/paix/Desktop/Python_lab/frame_data/20210610/temperature/" + laser_power + "_" + feed_rate + "_" + layer_number + "/"
                    if os.path.exists(save_path)!=True:
                        print('解析を開始します')
                        for i in range(count):
                            start = time.time()
                            ic(i)
                            img_CMOS = np.array(Image.open(dir_name + 'img_' + str(i) + '.bmp'))
                            # print(img_CMOS)
                            # img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/dstName.bmp'))
                            x,y = gp.get_gravitypoint_CMOS(img_CMOS, False)
                            trimmed_img_CMOS = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), :]

                            img_zero = np.zeros((height,width))
                            
                            threshold = 20
                            trimmed_img_CMOS = np.where(trimmed_img_CMOS > 20, trimmed_img_CMOS, 0)
                            if np.count_nonzero(trimmed_img_CMOS>0) > 100:
                                # index = trimmed_img_CMOS > 0
                                # ic(index.shape)

                                img_zero = trimmed_img_CMOS[:,:,0]*20.76836881 + trimmed_img_CMOS[:,:,1]*5.96208386 + trimmed_img_CMOS[:,:,2]*(-13.79605271)
                                img_zero = np.where(img_zero > 0, img_zero + 1451.05263058, 0)
                                # trimmed_img_r = trimmed_img_CMOS[:,:, 0]
                                # trimmed_img_g = trimmed_img_CMOS[:,:, 1]
                                # trimmed_img_b = trimmed_img_CMOS[:,:, 2]
                                
                                # img_zero = np.zeros(height*width)
                                
                                # threshold = 20
                                # img_red = trimmed_img_r[:,:].reshape(height*width)
                                # ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
                                # trimmed_img_r = trimmed_img_r.reshape(height*width)
                                # trimmed_img_g = trimmed_img_g.reshape(height*width)
                                # trimmed_img_b = trimmed_img_b.reshape(height*width)
                                # for j in img_thresh.nonzero():
                                #     img_zero[j] += trimmed_img_r[j]*20.76836881 + trimmed_img_g[j]*5.96208386 + trimmed_img_b[j]*(-13.79605271) + 1451.05263058
                                #     # R2 = 0.46292409520051325
                                # # ic(img_zero)
                                # # twocolor_CMOS = tc.tocolor(img_zero).reshape(height, width, 3)
                                # ic(img_zero)
                                # twocolor_CMOS = tc.tocolor(img_zero, height, width).reshape(height, width, 3)
                                twocolor_CMOS = tc.tocolor(np.reshape(img_zero, height*width), height, width).reshape(height, width, 3)

                                img_ave = np.array(twocolor_CMOS, dtype=np.int8)
                                pil_img = Image.fromarray(img_ave, mode="RGB")
                                save_name = 'img_' + str(i) + ".bmp"
                                # pil_img.save('calibration/time_average/colorimg/CMOS_int8_RGBmin' + str(threshold) + save_name)
                                
                                os.makedirs(save_path, exist_ok=True)
                                pil_img.save(save_path + save_name)
                                print(str(i) + 'はsaveしました。')
                                end = time.time()
                                elapsed_time4 = round(end - start, 3)
                                ic(elapsed_time4)
                            else:
                                print(str(i) + 'はsaveされませんでした。')
                                end = time.time()
                                elapsed_time5 = round(end - start, 3)
                                ic(elapsed_time5)
                                continue
                    else:
                        print('解析済みのデータのため飛ばしました')
                        continue
                else:
                    print('ディレクトリが存在しなかったため飛ばしました')
                    continue



    # RGBvalue = 1
    # CMOS = trimmed_img[:, :, RGBvalue]
    # height = 90
    # width = 120
    # RGBmin = 20
    # RGBmax = 255