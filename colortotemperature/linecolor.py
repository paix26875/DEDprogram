import cv2
from PIL import Image
import numpy as np

# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)

if __name__ == '__main__':
    print('which? high / low')
    mode = input()
    if mode == 'high':
        base_name = "/Users/paix/Desktop/Python_lab/colortotemperature/high/"
        img_sum = Image.open(base_name + "1310-1470.BMP")
        temp = 1475
    elif mode == 'low':
        base_name = "/Users/paix/Desktop/Python_lab/colortotemperature/low/"
        img_sum = Image.open(base_name + "800-960.BMP")
        temp = 965
        img_sum = np.array(img_sum)
    img_sum = img_sum[0 : 479, 655 : 656]
    img_sum = np.squeeze(img_sum)
    for i in range(0, 7):
        img_pil = Image.open(base_name + str(temp) + "-" + str(temp + 160) + ".BMP")
        img = np.array(img_pil)
        img_line = img[0 : 479, 655 : 656]
        img_2d = np.squeeze(img_line)
        print(img_2d.shape)
        # np.append(img_sum, img_2d)
        img_sum = np.concatenate([img_sum, img_2d])
        print(img_sum.shape)
        temp += 165
    np.savetxt('./np_savetxt.txt', img_sum, delimiter=',', fmt='%d')
    
    # img_cv2 = cv2.imread("/Users/paix/Desktop/Python_lab/colortotemperature/1300-1470.BMP")
    # cv2.imshow("image", img_cv2)
    # cv2.waitKey(0)
    # print(img_line.shape)
    # print(np.unique(img_line, axis=0))