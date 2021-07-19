import cv2
import numpy as np
from icecream  import ic
import gravitypoint as gp
import math

if __name__ == '__main__':
    # dir_path = "/Users/paix/Desktop/Python_lab/calibration/alignment/img/projection_accuracy/"
    # dir_path = input()
    dir_path = "/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/"
    # CMOS_path = dir_path + 'CMOS_transformed_date.bmp'
    # CMOS_path = dir_path + '/Users/paix/Desktop/Python_lab/frame_data/20210421/CMOS_after_projection.bmp'
    # CMOS_path = dir_path + 'CMOS_after_projection.bmp'
    CMOS_path = dir_path + 'CMOS_transformed_date_binary.bmp'
    pyrometer_path = dir_path + 'pyrometer_date.bmp'
    ic(CMOS_path)
    ic(pyrometer_path)

    # img_CMOS = cv2.imread(CMOS_path)[:,:,0]
    # ret, gray = cv2.threshold(img_CMOS, 200, 255, cv2.THRESH_BINARY)
    # invgray = cv2.bitwise_not(gray)
    # cv2.imshow('img', invgray)
    # cv2.waitKey(0)
    # x = np.array([270,300,365,390,270,295,180,205,264,290])
    # y = np.array([145,170,210,230,270,290,205,235,210,230])
    # x = np.array([12,44,10,40,20,50,270,300,540,570,530,580])
    # y = np.array([12,47,210,230,380,410,390,410,390,410,200,230])
    # 20210421
    x = np.array([296,316,288,308,294,321])
    y = np.array([202,222,135,155,259,276])
    CMOS = np.array([])
    pyrometer = np.array([])
    distance = np.array([])
    for i in range(0,len(x),2):
        ic(i)
        # img_CMOS = cv2.imread(CMOS_path)[y[i]:y[i+1], x[i]:x[i+1], 0:3]
        # img_pyrometer = cv2.imread(pyrometer_path)[y[i]:y[i+1], x[i]:x[i+1], 0:3]
        img_CMOS = cv2.imread(CMOS_path)[y[i]:y[i+1], x[i]:x[i+1], 0]
        img_pyrometer = cv2.imread(pyrometer_path)[y[i]:y[i+1], x[i]:x[i+1], 1]

        threshold = 200
        # gray = cv2.cvtColor(img_CMOS, cv2.COLOR_RGB2GRAY)
        ret, gray = cv2.threshold(img_CMOS, threshold, 255, cv2.THRESH_BINARY)
        invgray = cv2.bitwise_not(gray)
        x1, y1 = gp.get_gravitypoint_img_gray(invgray)
        CMOS = np.append(CMOS, [x1, y1])
        
        threshold = 75
        # gray = cv2.cvtColor(img_pyrometer, cv2.COLOR_RGB2GRAY)
        ret, gray = cv2.threshold(img_pyrometer, threshold, 255, cv2.THRESH_BINARY)
        invgray = cv2.bitwise_not(gray)
        x2, y2 = gp.get_gravitypoint_img_gray(invgray)
        pyrometer = np.append(pyrometer, [x2, y2])

        distance = np.append(distance, math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    ic(distance)
    ic(np.mean(distance))