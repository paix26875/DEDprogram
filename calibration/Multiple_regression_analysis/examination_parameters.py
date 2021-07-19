from PIL import Image
import numpy as np
import gravitypoint as gp
import twocolor_convert as tc
from icecream import ic
# import cv2
import os
import time
from matplotlib import pyplot as plt
import glob

np.set_printoptions(threshold=np.inf)

def linear_plot(array,laser_power, feed_rate, layer_number, count, title, label, save_as_file=False, show_graph=True):
    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']
    
    fig = plt.figure()
    ax = fig.subplots()

    ax.set_xlabel("フレーム", fontsize = 12)
    if label == "peak":
        ylabel = "ピーク温度 [℃]"
    elif label == "width":
        ylabel = "溶融地幅 [px]"
    elif label == "area":
        ylabel = "溶融地面積 [px]"
    ax.set_ylabel(ylabel, fontsize = 12)
    
    x = np.arange(0,count)
    ax.plot(x, array, label = label, color="red")
    ax.scatter(x, array, linestyle='solid', color="red")

    ax.legend()
    fig.subplots_adjust(bottom=0.2)
    condition = '条件：レーザ出力：' + str(laser_power) + ' W, ' + '走査速度：' + str(feed_rate) + ' mm/min, ' + 'layer：' + str(layer_number) + ' 層目'
    fig.text(0.02, 0.02, condition, fontsize=6)
    title = title
    fig.text(0.45, 0.05, title, fontsize=14)

    if label == "peak":
        ax.set_ylim(1500, 2500)
    elif label == "width":
        ax.set_ylim(0, 300)
    elif label == "area":
        ax.set_ylim(0, 30000)

    if save_as_file:
        os.makedirs("/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/1track/" + laser_power + "_" + feed_rate + "_" + layer_number + "/", exist_ok=True)
        fig.savefig("/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/1track/" + laser_power + "_" + feed_rate + "_" + layer_number + "/" + title + ".png")
    
    if show_graph:
        plt.show()
    else:
        plt.close()
    ic(np.median(array))
    ic(np.average(array))
    return np.average(array)

def save_3D_hist(temperature, laser_power, feed_rate, layer_number, count, shape='surface', save_as_file=False, show_graph=True):
    """
    温度のじかん
    """
    ic(temperature.shape)
    x = np.ones_like(temperature)
    h = 300
    w = 300
    ic(count)
    for i in range(1, count):
        x[h*w*i:] = i
    # ic(np.max(x))
    x = np.delete(x, np.where(temperature<20))
    y = np.delete(temperature ,np.where(temperature<20))
    # y = temperature
    # print(x.shape)
    # print(y)


    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']
    
    
    plt.style.use('ggplot')
    plt.rcParams["axes.facecolor"] = 'white'
    # ic(x)
    # ic(x.shape)
    # ic(x.size)
    # ic(count)
    ybins = int((np.amax(y) - np.amin(y)) / 20)
    xbins = count-1
    ic(ybins)
    # hist, xedges, yedges = np.histogram2d(x, y, bins=[count, 100], range=[[0, 4], [0, 4]])
    hist, xedges, yedges = np.histogram2d(x, y, bins=[xbins, ybins])
    # ic(hist)
    # ic(hist.shape)
    # ic(hist.size)
    ic(np.amax(y))
    ic(np.amin(y))
    bottom = int((np.amin(y) - 1500) / 20)
    if bottom == 0:
        bottom = 1
    top = int((2500 - np.amax(y)) / 20)
    if top == 0:
        top = 1
    ave = np.pad(np.average(hist, axis=0), [bottom, top], 'constant')
    if ave.size != 50:
        top = int(50 - ave.size)
        ave = np.pad(ave, [0, top], 'constant')

    # ave = np.average(hist, axis=0)
    # ic(np.average(hist, axis=0))
    # ic(ave.shape)
    # ic(np.average(hist, axis=0).size)
    # ic(xedges.shape)
    # ic(yedges.shape)
    # Construct arrays for the anchor positions of the 16 bars.
    # xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    # ic(xpos.shape)
    # ic(ypos.shape)
    # ic(hist.shape)
    # xpos = xpos.ravel()
    # ypos = ypos.ravel()
    zpos = 0
    dx = dy = 0.5
    dz = hist.ravel()
    fig = plt.figure(figsize=(12,5))

    ax = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)
    # # x2 = np.arange(np.amin(y), np.amax(y), 20)
    x2 = np.arange(1500, 2500, 20)
    ax2.plot(x2, ave, linestyle='solid', color="red")
    ax2.scatter(x2, ave, linestyle='solid', color="red")
    # # 軸ラベルの設定
    ax2.set_xlabel("温度 [℃]")
    ax2.set_ylabel("平均ピクセル数")
    # ax = Axes3D(fig)

    # Z = 500
    # pop=y
    # norm = plt.Normalize((Z/np.log10(max(pop))).min(), (Z/np.log10(max(pop))).max())
    # colours = plt.cm.rainbow_r(norm(Z/np.log10(max(pop))))
    if shape == "histgram":
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average', cmap='jet', alpha=0.4)
    elif shape == "surface":
        surface = ax.plot_surface(xpos, ypos, hist, rstride=1, cstride=10, cmap='jet', alpha=0.4, vmin=0, vmax=2000)
        cax = fig.add_axes((0.02, 0.3, 0.05, 0.5))
        fig.colorbar(surface, ax=ax, shrink=0.5, cax=cax)
        ic(xpos.shape)
        ic(ypos.shape)
        ic(hist.shape)
        # ic(xpos)
        # ic(ypos)
        # ic(hist)
    elif shape == "wire":
        ax.plot_wireframe(xpos, ypos, yedges, linewidth=0.3, cmap='jet', alpha=0.4)

    # colourMap = plt.cm.ScalarMappable(cmap=plt.cm.rainbow_r)
    # colourMap.set_array(Z)
    # colBar = plt.colorbar(colourMap).set_label('log\u2081\u2080(Population)')

    # 表示範囲の設定
    ax.set_xlim(0, count)
    ax.set_ylim(1500, 2500)
    ax.set_zlim(0, 2000)

    # 軸ラベルの設定
    ax.set_xlabel("フレーム")
    ax.set_ylabel("温度")
    ax.set_zlabel("ピクセル数")

    # タイトル設定
    fig.subplots_adjust(bottom=0.2)
    condition = '条件：レーザ出力：' + str(laser_power) + ' W, ' + '走査速度：' + str(feed_rate) + ' mm/min, ' + 'layer：' + str(layer_number) + ' 層目'
    fig.text(0.02, 0.02, condition, fontsize=6)
    title = "温度ヒストグラムの時間変化"
    fig.text(0.30, 0.05, title, fontsize=14)

    ax.view_init(elev=45,azim=310)
    
    if save_as_file:
        os.makedirs("/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/3Dhistgram2/1track/" + laser_power + "_" + feed_rate + "_" + layer_number + "/", exist_ok=True)
        fig.savefig("/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/3Dhistgram2/1track/" + laser_power + "_" + feed_rate + "_" + layer_number + "/" + shape + ".png")
    if show_graph:
        plt.show()
    else:
        plt.close()
    return ave

def width():
    pass
def area():
    pass

if __name__ == '__main__':
    laser_power = "1600"
    # feed_rate = "1250"
    feed_rate = "1000"
    layer_number = "11"
    all_hist = np.array([])
    peak = np.array([])
    width = np.array([])
    area = np.array([])
    laser_list = ['1000', '1200', '1400', '1600', '1800', '2000']
    feed_list = ['625', '750', '875', '1000', '1125', '1250']
    # for laser_power in ['1000', '1200', '1400', '1600', '1800', '2000']: # レーザ出力
    # for feed_rate in ['625', '750', '875', '1000', '1125', '1250']: # 走査速度
    # for laser_power, feed_rate in zip(laser_list, feed_list): # EF値一定 
        # for layer_number in ['1', '5', '11']:
    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210610/temperature/" + laser_power + "_" + feed_rate + "_" + layer_number + "/"
    if os.path.exists(dir_name):
        files = os.listdir(dir_name)
        count = len(files)
        
        all_peak = np.array([])
        all_temp = np.array([])
        all_width = np.array([])
        all_area = np.array([])
        for file in sorted(glob.glob(dir_name + "*")):
            # ic(i)
            ic(file)
            # img = np.array(Image.open(dir_name + "/img_" + str(i) + ".bmp"))
            img = np.array(Image.open(file))
            temperature_np = np.round(tc.totemperature(img), -1)
            all_peak = np.append(all_peak, temperature_np.max())
            all_temp = np.append(all_temp, temperature_np.reshape(-1))
            all_width = np.append(all_width, np.amax(np.sum(np.where(temperature_np > 20, 1, 0), axis=1)))
            all_area = np.append(all_area, np.sum(np.sum(np.where(temperature_np > 20, 1, 0), axis=1)))
        outliers = 3 #外れ値の指定（最初と最後の数フレームは外れ値になる）
        all_temp = all_temp[outliers * 90000 : count - outliers * 90000]
        all_peak = all_peak[outliers : count - outliers]
        all_width = all_width[outliers : count - outliers]
        all_area = all_area[outliers : count - outliers]
        ic(all_temp.shape)
        ave = save_3D_hist(all_temp, laser_power, feed_rate, layer_number, count-outliers*2, save_as_file=True, show_graph=False)
        # ave_peak = linear_plot(all_peak, laser_power, feed_rate, layer_number, count-outliers*2, 'peak', 'peak', save_as_file=False, show_graph=False)
        # ave_width = linear_plot(all_width, laser_power, feed_rate, layer_number, count-outliers*2, 'width', 'width', save_as_file=False, show_graph=False)
        # ave_area = linear_plot(all_area, laser_power, feed_rate, layer_number, count-outliers*2, 'area', 'area', save_as_file=False, show_graph=False)
        # all_hist = np.append(all_hist, ave)
        # peak = np.append(peak, ave_peak)
        # width = np.append(width, ave_width)
        # area = np.append(area, ave_area)
    
    # np.savetxt('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/csv/EFconstant_peak.csv',peak,delimiter=',')
    # np.savetxt('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/csv/EFconstant_width.csv',width,delimiter=',')
    # np.savetxt('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/csv/EFconstant_area.csv',area,delimiter=',')
    # ic(all_hist)
    # ic(all_hist.shape)
    # ic(all_hist.size)
    # x = np.ones_like(all_hist)
    # y = np.ones_like(all_hist)
    # for i in range(1, 7):
    #     laser = 800 + 200 * i
    #     ic(laser)
    #     x[50*(i-1):] = laser
    # ic(x)
    # for i in range(1, 50):
    #     temp = 1480 + 20*i
    #     ic(temp)
    #     y[6*(i-1):] = temp
    # ic(y)
    # x = x.reshape(6, 50)
    # y = y.reshape(6, 50)
    # all_hist = all_hist.reshape(6, 50)
    # ic(all_hist)
    # fig = plt.figure(figsize=(5,5))
    # ax = fig.add_subplot(111, projection='3d')
    # surface = ax.plot_surface(x, y, all_hist, rstride=1, cstride=10, cmap='jet', alpha=0.4)
    # cax = fig.add_axes((0.02, 0.3, 0.05, 0.5))
    # fig.colorbar(surface, ax=ax, shrink=0.5, cax=cax)
    # plt.show()

    # all_hist = all_hist.T
    # h, w = all_hist.shape 
    # #h=262, w=20 
    # fig = plt.figure(num=None, dpi=80,figsize=(9, 7)) 
    # ax = fig.add_subplot(111) 
    # #fig, ax = plt.subplots() 
    # plt.imshow(all_hist) 
    # plt.colorbar() 
    # plt.xticks(np.arange(w), ['1000', '1200', '1400', '1600', '1800', '2000']) 
    # ax.set_aspect(w/h) 
    # plt.show()
