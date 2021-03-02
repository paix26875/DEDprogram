import cv2

filepath = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1400/img_181.bmp"
filepath = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/zennbu.BMP"
filepath1 = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper/CMOS_114.bmp"
filepath2 = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper/twodolorper.bmp"
filepath3 = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1600-164-3805.BMP"
img = cv2.imread(filepath)
# 閾値の設定
threshold = 20
# 二値化(閾値100を超えた画素を255にする。)
ret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
img1 = cv2.imread(filepath1)
img2 = cv2.imread(filepath2)
img3 = cv2.imread(filepath3)
cv2.imshow("img", img)
# cv2.imshow("img", img_thresh)
# cv2.imshow("img", img1)
# cv2.imshow("img", img2)
# cv2.imshow("img", img3)
cv2.waitKey(0)
