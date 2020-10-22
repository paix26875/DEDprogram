from PIL import Image
import numpy as np
import os
import time

"""
ディレクトリ内のファイル数をカウントする
引数：ディレクトリのパス(str)
戻り値：ファイルの数(int)
"""
def count_file_in_dir(path): 
    files = os.listdir(path)  
    count = len(files)  
    return count

"""
画像ファイルをR値のみを入れたnumpy配列に変換する
引数：画像
戻り値：画像のR値が格納されたnumpy配列
"""
def convert_img_to_numpy(img):
    img_np = np.array(img)#画素値numpy化
    img_r = img_np[:, :, 2]#画像のR値のみ抜き出し
    return img_r



"""
画像の中心線上にR>20のピクセルが存在するかを判定する
溶融池が写っているフレームのインデックスを特定
引数：n枚目の画像のR値が格納された2次元配列
戻り値：bool値
"""
def is_valid_meltpool_img(img_r):
    h,w = img_r.shape
    half_width = int(w/2)
    img_center_col = img_r[:,half_width]
    if np.any(img_center_col > 20):
        return True
    else:
        return False



