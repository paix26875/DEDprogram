import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


if __name__ == '__main__':
    print("filter:")
    # filter = input()
    filter = '84'
    print("laser power:")
    laser_power = input()

    # for filter in (["83", "84", "84-2", "85"]):
    #     for laser_power in range(1200, 2200, 200):
    path = "/Users/paix/Desktop/Python_lab/frame_data/20201123/" + filter + "/" + str(laser_power) + "/"
    print(path)
    files = os.listdir(path)  
    count = len(files)  
    print(count)
    img = np.array(Image.open(path + "img_0.bmp"))
    h,w,l=img.shape
    R = np.reshape(img[:,:,0], h*w)
    G = np.array([])
    B = np.array([])

    for i in range(1,count):
        img = np.array(Image.open(path + "img_" + str(i) + ".bmp"))
        h,w,l=img.shape
        # h, w= img.shape
        R = np.append(R, np.reshape(img[:,:,0], h*w))
        # G = np.append(G, np.reshape(img[:,:,1], h*w))
        # B = np.append(B, np.reshape(img[:,:,2], h*w))
    print(R.shape)


    x = np.ones_like(R)
    for i in range(1, count):
        x[h*w*i:] = i
    x = np.delete(x, np.where(R<35))
    y = np.delete(R,np.where(R<35))
    print(x.shape)
    print(y.shape)

    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

    fig = plt.figure()
    ax = fig.add_subplot(111)

    H = ax.hist2d(x ,y , bins=[count, 200], cmap=cm.jet)
    ax.set_xlabel('フレーム')
    ax.set_ylabel('RGB値')
    fig.colorbar(H[3],ax=ax)
    
    fig.subplots_adjust(bottom=0.2)
    title = 'フィルタ：' + filter + '/レーザ出力：' + str(laser_power) + ' W'
    fig.text(0.25, 0.02, title, fontsize=14)
    plt.show()