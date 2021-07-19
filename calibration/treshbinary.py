import cv2

# 画像の読み込み
# img1 = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/perspective/img_117.bmp", 0)
img1 = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20200202/2000/img_88.bmp", 0)

# 閾値の設定
threshold = 25
# 二値化(閾値100を超えた画素を255にする。)
ret, img_thresh1 = cv2.threshold(img1, threshold, 255, cv2.THRESH_BINARY_INV)
# ret, img_thresh1 = cv2.threshold(img_thresh1, threshold, 255, cv2.THRESH_BINARY_INV)

img2 = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20200202/1600/img_133.bmp", 0)
# threshold = 30
ret, img_thresh2 = cv2.threshold(img2, threshold, 255, cv2.THRESH_BINARY_INV)


# 二値化画像の表示
# cv2.imwrite("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/per/CMOS_114.bmp", img_thresh)
# cv2.imwrite("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/per/twocolor.bmp", img_thresh)
# cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow("img_th1", img_thresh1)
cv2.waitKey(0)
cv2.imshow("img_t2", img_thresh2)
cv2.waitKey(0)
# cv2.destroyAllWindows()
# color_hist("/Users/paix/Desktop/Python_lab/frame_data/20200202/2000/img_88.bmp")
# color_hist("/Users/paix/Desktop/Python_lab/frame_data/20200202/1600/img_133.bmp")