from PIL import Image
import os
from icecream import ic
import numpy as np
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

if __name__ == '__main__':
    width = 120
    height = 90
    w = -width
    dst = Image.new('RGB', (width*5, height*1))
    for laser_power in range(1400,1900,100):
        # layer_number = '1'
        h = 0
        w += width
        # dir_name = "/Users/paix/Documents/Research/M2打ち合わせ/第7回打ち合わせ資料/peak/" + filter + '/'
        # dir_name = "/Users/paix/Documents/Research/M2打ち合わせ/第8回打ち合わせ資料/時間平均画像/"
        # dir_name = "/Users/paix/Documents/Research/M2打ち合わせ/第8回打ち合わせ資料/f4g16/"
        dir_name = "/Users/paix/Documents/Research/M2打ち合わせ/第8回打ち合わせ資料/f4g24/"
        if os.path.exists(dir_name):
            # img = Image.open(dir_name + laser_power + "_" + layer_number + '.png')
            # img = np.array(Image.open(dir_name + str(laser_power) + '.bmp'))[150-60:150+60, 150-45:150+45]
            img = np.array(Image.open(dir_name + str(laser_power) + '.bmp'))[150-45:150+45, 150-60:150+60]
            pil_img = Image.fromarray(img, mode="RGB")
            pil_img.save(dir_name + str(laser_power) + 'trim.bmp')
            img = Image.open(dir_name + str(laser_power) + 'trim.bmp')
            ic(w,h)
            dst.paste(img, (w, h))    
    dst.save(dir_name + 'all2.png')