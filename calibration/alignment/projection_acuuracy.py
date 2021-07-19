import cv2
import numpy as np
from icecream  import ic
import projection_transformation as pt
import gravitypoint_copy as gp

if __name__ == '__main__':
    # # ic| gravitypoint_x: 60, gravitypoint_y: 34CMOS
    # # ic| gravitypoint_x: 13, gravitypoint_y: 8py
    # # ic| gravitypoint_x: 40, gravitypoint_y: 43CMOS
    # # ic| gravitypoint_x: 10, gravitypoint_y: 14py

    # # ic| gravitypoint_x: 38, gravitypoint_y: 44
    # # ic| gravitypoint_x: 15, gravitypoint_y: 8

    # # ic| gravitypoint_x: 41, gravitypoint_y: 51
    # # ic| gravitypoint_x: 18, gravitypoint_y: 9
    # #変換前の4点の座標
    # # CMOS_pts = np.array([[220, 225], [637, 150], [752, 409], [332, 509]], dtype=np.float32)# トリミング：[1000:1800, 1650:2650, 0:3]
    # # CMOS_pts = np.array([[1650 + 220, 1000 + 225], [1650 + 637, 1000 + 150], [1650 + 752, 1000 + 409], [1650 + 332, 1000 + 509]], dtype=np.float32)# [1000:1800, 1650:2650, 0:3]
    # # CMOS_pts = np.array([[1400 + 49, 1350 + 34], [1880 + 39, 880 + 49], [2660 + 36, 1130 + 45], [2260 + 37, 1650 + 50]], dtype=np.float32)# garavity point
    # # CMOS_pts = np.array([[1400 + 60, 1350 + 34], [1880 + 40, 880 + 43], [2660 + 38, 1130 + 44], [2260 + 41, 1650 + 51]], dtype=np.float32)# garavity point
    # # #変換後の4点の座標
    # # # pyrometer_pts = np.array([[279, 183], [370, 246], [280,301], [190, 243],], dtype=np.float32)
    # # # pyrometer_pts = np.array([[140 + 12, 110 + 14], [400 + 14, 110 + 14], [400 + 14, 300 + 12], [140 + 14, 295 + 12]], dtype=np.float32)# gravity point
    # # pyrometer_pts = np.array([[140 + 13, 110 + 8], [400 + 10, 110 + 14], [400 + 15, 300 + 8], [140 + 18, 295 + 9]], dtype=np.float32)# gravity point
    # # mat = pt.projection_matrix(CMOS_pts, pyrometer_pts)
    # # 20210421
    # #変換前の4点の座標[y, x]
    # src_pts = np.array([[190,374], [490,370], [477,572], [192,564]], dtype=np.float32)
    # #変換後の4点の座標
    # dst_pts = np.array([[258,185], [345,187], [342,250], [262,245]], dtype=np.float32)
    # mat = pt.projection_matrix(src_pts, dst_pts)

    # dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/"
    # CMOS = cv2.imread(dir_name + "CMOS_date.bmp")
    # cv2.imshow("image", CMOS)
    # cv2.waitKey(0)
    # pyrometer = cv2.imread(dir_name + "pyrometer_date.bmp")
    # cv2.imshow("image", pyrometer)
    # cv2.waitKey(0)
    # h, w, c = CMOS.shape
    
    # if w < 640:
    #     CMOS_transformed = cv2.warpPerspective(CMOS, mat, (640, h))[0 : 480, 0 : 640, 0:3]
    # else:
    #     CMOS_transformed = cv2.warpPerspective(CMOS, mat, (w, h))[0 : 480, 0 : 640, 0:3]
    # cv2.imshow('image', CMOS_transformed)
    # cv2.waitKey(0)
    # CMOS_red = pt.img_change_color(CMOS_transformed, "blue")
    # # cv2.imshow('image', CMOS_red)
    # # cv2.waitKey(0)
    # ic(CMOS_red.shape)
    # pyrometer_blue = pt.img_change_color(pyrometer, "red")
    # # cv2.imshow('image', pyrometer_blue)
    # # cv2.waitKey(0)
    # ic(pyrometer_blue.shape)
    
    # img_compare = pt.img_overray(CMOS_red, pyrometer_blue, 30)
    # cv2.imwrite("/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/CMOS_transformed_date_binary.bmp", CMOS_transformed)
    # cv2.imwrite("/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/img_compare_date_binary.bmp", img_compare)
    
    
    
    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/"
    CMOS = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g16/1600/img_31.bmp")
    x,y = gp.get_gravitypoint_CMOS(CMOS)
    CMOS = CMOS[ y - 45 : y + 45 , x - 60 : x + 60]
    cv2.imshow("image", CMOS)
    cv2.waitKey(0)
    pyrometer = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20210706/colorimg/1600_101.bmp")
    cv2.imshow("image", pyrometer)
    cv2.waitKey(0)
    CMOS_red = pt.img_change_color(CMOS, "blue")
    pyrometer_blue = pt.img_change_color(pyrometer, "red")
    img_compare = pt.img_overray(CMOS_red, pyrometer_blue, 30)
    cv2.imwrite("/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/img_compare_meltpool.bmp", img_compare)