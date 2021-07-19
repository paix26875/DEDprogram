import numpy as np
from PIL import Image
import os

def countFile(dirname):
    number = sum(os.path.isfile(os.path.join(dirname, name)) for name in os.listdir(dirname))
    return number

def imgIndex(dirname):
    number = countFile(dirname)
    index = np.zeros(number)
    for i in range(0, number):
        filename = dirname + "/img_" + str(i) + ".bmp"
        img = np.asarray(Image.open(filename).convert("RGB"))
        if (np.any(img>50)):
            index[i] = 1
            # print(np.max(img))
    return index



if __name__ == "__main__":
    print(imgIndex("frame_data/20201123/84-1400"))
    # print(np.sum(imgIndex("frame_data/20201123/84-1400")))
