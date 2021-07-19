import sys
import cv2
import os
import glob
import numpy as np

if __name__ == '__main__':
    print("filter:")
    # filternum = input()
    # filter = '83'
    filters = (["f4g8", "f4g32", "f5g32", "f5g64"])
    print("laser power:")
    # laser_power = input()
    laser_powers = (["1200", "1600", "2000"])
    print("layer:")
    # layer = input()
    layers = (["1", "5", "11"])
    # for filter, laser_power, layer in zip(filters, laser_powers, layers):
    for filter in filters:
        for laser_power in laser_powers:
            for layer in layers:
                path = "/Users/paix/Desktop/Python_lab/frame_data/20210629/" + filter + "/" + laser_power + '_' + layer + "/"
                print(path)
                files = os.listdir(path)  
                count = len(files)  
                print(count)
                img_array = []
                files = os.listdir(path)
                count = len(files) 
                # for filename in sorted(glob.glob(dir_name + "*.BMP")):
                for filenum in range(0, count):
                    filename = path + "img_" + str(filenum) + ".bmp"
                    print(filename)
                    img = cv2.imread(filename)
                    h,w,l = img.shape
                    img = np.where(img >= 255, 0, img)
                    img = img[int(h*4/12):int(h*7/12), int(w/3):int(w*2/3), :]
                    height, width, layerss = img.shape
                    size = (width, height)
                    img_array.append(img)

                os.makedirs("/Users/paix/Documents/Research/M2打ち合わせ/第7回打ち合わせ資料/video/" + filter + "/", exist_ok=True)
                name = "/Users/paix/Documents/Research/M2打ち合わせ/第7回打ち合わせ資料/video/" + filter + "/" + str(laser_power) + layer + ".mp4"

                out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MP4V'), 15.0, size)

                for i in range(len(img_array)):
                    out.write(img_array[i])
                out.release()

