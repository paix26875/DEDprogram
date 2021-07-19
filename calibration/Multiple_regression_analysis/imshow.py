import cv2
from PIL import Image
import numpy as np

if __name__ == '__main__':
    path = '/Users/paix/Desktop/Python_lab/frame_data/20210706/pyro/1600/16000OUT4845.BMP'
    # img = np.array(Image.open(path))
    img = cv2.imread(path)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    