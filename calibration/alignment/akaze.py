# https://campkougaku.com/2020/04/15/alignment/

##
# @file alignment.py
# @date 2020/4/14
# @brief 複数画像の位置合わせモジュール

import cv2
import numpy as np

##
# @brief AKAZEによる画像特徴量取得
# @param img 特徴量を取得したい画像（RGB順想定）
# @param pt1 特徴量を求める開始座標 tuple (default 原点)
# @param pt2 特徴量を求める終了座標 tuple (default None=画像の終わり位置)
# @return key points
def get_keypoints(img, pt1 = (0, 0), pt2 = None):

    if pt2 is None:
        pt2 = (img.shape[1], img.shape[0])

    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = img
    mask = cv2.rectangle(np.zeros_like(gray), pt1, pt2, color=1, thickness=-1)
    sift = cv2.AKAZE_create()

    # find the key points and descriptors with AKAZE
    return sift.detectAndCompute(gray, mask=mask)
##
# @brief imgと、特徴記述子kp2/des2にマッチするような pointを求める
# @param img 特徴量を取得したい画像（RGB順想定）
# @param kp2 ベースとなる画像のkeypoint
# @param des2 ベースとなる画像の特徴記述
# @return apt1 imgの座標　apt2 それに対応するkp2
def get_matcher(img, kp2, des2):

    kp1, des1 = get_keypoints(img)

    if len(kp1) == 0 or len(kp2) == 0:
        return None

    # Brute-Force Matcher生成
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) == 0:
        return None

    target_position = []
    base_position = []
    # x,y座標の取得
    for g in good:
        target_position.append([kp1[g.queryIdx].pt[0], kp1[g.queryIdx].pt[1]])
        base_position.append([kp2[g.trainIdx].pt[0], kp2[g.trainIdx].pt[1]])

    apt1 = np.array(target_position)
    apt2 = np.array(base_position)
    return apt1, apt2

##
# @brief マッチング画像生成(kp2にマッチするような画像へimgを変換)
# @param img 変換させる画像（RGB順想定）
# @param kp2 ベースとなる画像のkeypoint
# @param des2 ベースとなる画像の特徴記述
# @return アフィン変換後の画像 (行列推定に失敗するとNoneが返る)
def get_alignment_img(img, kp2, des2):

    height, width = img.shape[:2]
    # 対応点を探索
    apt1, apt2 = get_matcher(img, kp2, des2)

    # アフィン行列の推定
    mtx = cv2.estimateAffinePartial2D(apt1, apt2)[0]

    # アフィン変換
    if mtx is not None:
        return cv2.warpAffine(img, mtx, (width, height))
    else:
        return None


from icecream  import ic
import projection_transformation as pt
from PIL import Image



if __name__ == '__main__':

    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/alignment/"
    CMOS = np.array(Image.open(dir_name + "CMOS_date.bmp"))[:800,:,0]
    ret, CMOS = cv2.threshold(CMOS, 110, 255, cv2.THRESH_BINARY)
    cv2.imshow("image", CMOS)
    cv2.waitKey(0)
    pyrometer = np.array(Image.open(dir_name + "pyrometer_date.bmp"))[100:300,200:360,1]
    ret, pyrometer = cv2.threshold(pyrometer, 75, 255, cv2.THRESH_BINARY)
    cv2.imshow("image", pyrometer)
    cv2.waitKey(0)
    # h, w, c = CMOS.shape
    h, w = CMOS.shape
    kp, des = get_keypoints(pyrometer)
    ic(kp)
    ic(des)
    align = get_alignment_img(CMOS, kp, des)
    Image.fromarray(align[0 : 480, 0 : 640]).save(dir_name + "/akaze_CMOS_transformed_date.bmp", "bmp")
    # Image.fromarray(align[:,:]).save(dir_name + "/akaze_CMOS_transformed_date.bmp", "bmp")

    # apt1, apt2 = get_matcher(CMOS, kp, des)
    # ic(apt1)
    # ic(apt2)
    
    # mat = pt.projection_matrix(apt1, apt2)
    

    
    # CMOS_transformed = cv2.warpPerspective(CMOS, mat, (w, h))[0 : 480, 0 : 640, 0:3]
    # CMOS_red = pt.img_change_color(CMOS_transformed, "blue")
    # pyrometer_blue = pt.img_change_color(pyrometer, "red")
    
    # img_compare = pt.img_overray(CMOS_red, pyrometer_blue, 1)
    # Image.fromarray(CMOS_transformed).save("/Users/paix/Desktop/Python_lab/calibration/alignment/img/projection_accuracy/akaze_CMOS_transformed_date.bmp")
    # Image.fromarray(img_compare).save("/Users/paix/Desktop/Python_lab/calibration/alignment/img/projection_accuracy/akaze_img_compare_date.bmp")
    