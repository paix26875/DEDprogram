import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

def save_3D_hist(RGB, color, filter, laser_power, layer, isSave=False):

    x = np.ones_like(RGB)
    for i in range(1, count):
        x[h*w*i:] = i
    x = np.delete(x, np.where(RGB<20))
    y = np.delete(R,np.where(RGB<20))
    print(x.shape)
    print(y.shape)


    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']
    
    
    plt.style.use('ggplot')
    plt.rcParams["axes.facecolor"] = 'white'

    # hist, xedges, yedges = np.histogram2d(x, y, bins=[count, 100], range=[[0, 4], [0, 4]])
    hist, xedges, yedges = np.histogram2d(x, y, bins=[count, 100])
    # Construct arrays for the anchor positions of the 16 bars.
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    dx = dy = 0.5
    dz = hist.ravel()
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111, projection='3d')
    # ax = Axes3D(fig)

    # Z = 500
    # pop=y
    # norm = plt.Normalize((Z/np.log10(max(pop))).min(), (Z/np.log10(max(pop))).max())
    # colours = plt.cm.rainbow_r(norm(Z/np.log10(max(pop))))

    # ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average', color=colours)
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average', color=color)

    # colourMap = plt.cm.ScalarMappable(cmap=plt.cm.rainbow_r)
    # colourMap.set_array(Z)
    # colBar = plt.colorbar(colourMap).set_label('log\u2081\u2080(Population)')

    # 表示範囲の設定
    ax.set_xlim(0, count)
    ax.set_ylim(15, 256)
    ax.set_zlim(0, 200)

    # 軸ラベルの設定
    ax.set_xlabel("フレーム")
    if color == "red":
        ax.set_ylabel("R")
    elif color == "green":
        ax.set_ylabel("G")
    elif color == "blue":
        ax.set_ylabel("B")
    ax.set_zlabel("ピクセル数")

    # タイトル設定
    fig.subplots_adjust(bottom=0.2)
    title = 'フィルタ：' + filter + '/レーザ出力：' + str(laser_power) + ' W'
    fig.text(0.2, 0.02, title, fontsize=12)

    ax.view_init(elev=55,azim=310)
    
    # plt.show()

    if isSave:
        os.makedirs("/Users/paix/Documents/Research/M2打ち合わせ/第8回打ち合わせ資料/histgram1/" + filter + "/" + str(laser_power) + "/", exist_ok=True)
        fig.savefig("/Users/paix/Documents/Research/M2打ち合わせ/第8回打ち合わせ資料/histgram1/" + filter + "/" + str(laser_power) + "/" + color + ".png")
        plt.close


if __name__ == '__main__':
    
    print("filter:")
    # filternum = input()
    # filter = '83'
    filters = (["f4-g16", "f4-g24"])
    print("laser power:")
    # laser_power = input()
    laser_powers = (["1400", "1600", "2000"])
    print("layer:")
    # layer = input()
    layers = (["1", "5", "11"])
    # for filter, laser_power, layer in zip(filters, laser_powers, layers):
    for filter in filters:
        for laser_power in range(1400,1900,100):

            # for filter in (["83", "84", "84-2", "85"]):
            #     for laser_power in range(1200, 2200, 200):
            path = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/" + filter + "/" + str(laser_power) + "/"
            print(path)
            files = os.listdir(path)  
            count = len(files)  
            print(count)
            img = np.array(Image.open(path + "img_0.bmp"))
            h,w,l=img.shape
            R = np.reshape(img[:,:,0], h*w)
            G = np.reshape(img[:,:,1], h*w)
            B = np.reshape(img[:,:,2], h*w)

            for i in range(1,count):
                img = np.array(Image.open(path + "img_" + str(i) + ".bmp"))
                h,w,l=img.shape
                # h, w= img.shape
                R = np.append(R, np.reshape(img[:,:,0], h*w))
                G = np.append(G, np.reshape(img[:,:,1], h*w))
                B = np.append(B, np.reshape(img[:,:,2], h*w))
            # print(R.shape)
            save_3D_hist(R, "red", filter, laser_power, 0, isSave=True)
            save_3D_hist(G, "green", filter, laser_power, 0, isSave=True)
            save_3D_hist(B, "blue", filter, laser_power, 0, isSave=True)

