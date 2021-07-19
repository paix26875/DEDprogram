"""
画像を特定範囲でトリミングする
"""
import cv2

def img_trimming(img, top, bottom, left, right):
    """
    画像をトリミングする

    Parameters
    ----------
    img : numpy
        トリミングしたい画像のnumpy配列
    top : int
        トリミング範囲の上端
    bottom : int
        トリミング範囲の下端
    left : int
        トリミング範囲の左端
    right : int
        トリミング範囲の右端

    Returns
    -------
    trimmed_img : numpy
        トリミング後の画像
    """
    trimmed_img = img[top : bottom, left : right]
    return trimmed_img

if __name__ == '__main__':
    from PIL import Image
    import numpy as np
    import gravitypoint as gp
    img = np.array(Image.open("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp"))
    x,y = gp.get_gravitypoint_CMOS(img)
    trimmed_img = img[ y - 45 : y + 45 , x - 60 : x + 60]
    img_ave = np.array(trimmed_img, dtype=np.int8)
    pil_img = Image.fromarray(img_ave, mode="RGB")
    pil_img.save('calibration/time_average/colorimg/1600_300.bmp')