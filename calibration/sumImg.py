import glob
import cv2
import numpy as np
from icecream import ic

##画像の加算合成##

# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)

# 153〜171

src = "frame_data/20201123/10/afterper2/1600/img_"    #ソースの写真群がある場所    
sums = cv2.imread(src + "0.bmp").astype(np.uint32)
for fnum in range(153, 171):
    sums += cv2.imread(src + str(fnum) + ".bmp")
cv2.imwrite("dstName.bmp", (sums/19))    #平均化