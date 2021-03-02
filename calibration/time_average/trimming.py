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
    img = cv2.imread("/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolor/1600-164-3805.BMP")
    trimmed_img = img_trimming(img, 150, 300, 250, 400)
    cv2.imshow("image", trimmed_img)
    cv2.waitKey(0)