import cv2
from PIL import Image
import numpy as np
from icecream import ic
import gravitypoint as gp
import trimming as tr
import twocolor_convert as tc
from matplotlib import pyplot as plt
import os
import pandas as pd


# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)



if __name__ == '__main__':

    # レーザ出力とフレーム数の設定
    laser_power = 1600
    frames = 300
    begin_frame_number = 3755
    end_frame_number = begin_frame_number + frames
    # begin_frame_number = 3755
    # end_frame_number = 3765
    # begin_frame_number = 3755
    # end0_frame_number = 3855
    RGBvalue = 0
    height = 90
    width = 120
    RGBmin = 20
    RGBmax = 255

    # pathの設定
    total_frame_number = end_frame_number - begin_frame_number + 1
    directory_name = "/Users/paix/Desktop/Python_lab/frame_data/20201123/10/twocolors/"
    base_name = directory_name + str(laser_power) + "_600/" + str(laser_power) + "0OUT"
    color_img_path = 'calibration/time_average/colorimg/' + str(laser_power) + "_" + str(total_frame_number) + ".bmp"
    if os.path.exists(color_img_path):
    # if False:
        img_pil = Image.open(color_img_path)
        img_np = np.array(img_pil)
        temperature_ave = tc.totemperature(img_np)
        TEMP = temperature_ave# 1次元配列
        TEMPplt = temperature_ave.reshape(90*120)# 2次元配列
    else:
    # 温度の時間平均算出開始
        # 1枚目の溶融池画像を格納
        img_pil = Image.open(base_name + str(begin_frame_number) + ".BMP")
        img_np = np.array(img_pil)
        rough_trimmed_img = tr.img_trimming(img_np, 220, 310, 640, 1279)
        x, y = gp.get_gravitypoint_img(rough_trimmed_img)
        trimmed_img = rough_trimmed_img[ : , x - 60 : x + 60]
        # 温度データに変換 ######
        temperature_sum = tc.totemperature(trimmed_img)

        for frame_number in range(begin_frame_number + 1, end_frame_number + 1):
            # 1枚ずつ重心周りでトリミングしていく
            img_pil = Image.open(base_name + str(frame_number) + ".BMP")
            img_np = np.array(img_pil)
            rough_trimmed_img = tr.img_trimming(img_np, 220, 310, 640, 1279)
            x, y = gp.get_gravitypoint_img(rough_trimmed_img)# うまくいった
            trimmed_img = rough_trimmed_img[ : , x - 60 : x + 60]
            
            # 色データから温度データに変換 ######
            temperature_np = tc.totemperature(trimmed_img)
            temperature_sum += temperature_np

        total_frame_number = end_frame_number - begin_frame_number + 1
        temperature_ave = temperature_sum / total_frame_number
        TEMP = temperature_ave# 1次元配列
        TEMPplt = temperature_ave.reshape(90*120)# 2次元配列
        # # 温度ヒストグラム表示
        # plt.hist(TEMPplt, color="red", bins=128)
        # plt.ylim(0, 200)
        # plt.xlim(1300, 3000)
        # plt.show()
        ic(temperature_ave.shape)
        # # 温度データから色データに再変換
        img_ave = tc.tocolor(temperature_ave)
        # 平均化した溶融池温度分布の色画像を表示
        img_ave = np.array(img_ave, dtype=np.int8)
        pil_img = Image.fromarray(img_ave, mode="RGB")
        save_name = str(laser_power) + "_" + str(total_frame_number) + ".bmp"
        pil_img.save('calibration/time_average/colorimg/' + save_name)
    # 温度の時間平均算出終了




    # # キャリブレーション
    # if laser_power == 1400:
    #     img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1400/img_181.bmp'))
    # elif laser_power == 1600:
    #     img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1600/img_164.bmp'))
    # elif laser_power == 1800:
    #     img_CMOS = np.array(Image.open('/Users/paix/Desktop/Python_lab/frame_data/20201123/10/afterper2/1800/img_177.bmp'))
        
    # x,y = gp.get_gravitypoint_CMOS(img_CMOS)
    # trimmed_img = img_CMOS[ y - 45 : y + 45 , x - 60 : x + 60]
    # CMOS_r = trimmed_img[:, :, 0]
    # CMOS_g = trimmed_img[:, :, 1]
    # CMOS_b = trimmed_img[:, :, 2]

    # CMOS = trimmed_img[:, :, RGBvalue]
    # TEMP = TEMP.reshape(90*120)
    # CMOS_r = CMOS_r.reshape(90*120)
    # CMOS_g = CMOS_g.reshape(90*120)
    # CMOS_b = CMOS_b.reshape(90*120)

    # data = np.vstack([TEMP, CMOS_r, CMOS_g, CMOS_b])
    # # np.savetxt('/Users/paix/Desktop/Python_lab/calibration/time_average/data/temp/np_savetxt.csv', data.T, delimiter=',', fmt='%d')
    # df = pd.read_csv('/Users/paix/Desktop/Python_lab/calibration/time_average/data/temp/np_savetxt.csv', sep=',')
    # df.head()
    # x = df[['R', 'G']]
    # y = df[['temperature']]
    # x1 = df[['R']]
    # x2 = df[['G']]
    # ic(x.shape)
    # ic(y.shape)
    # x = x.values
    # y = y.values
    # index = np.all(x > 20, axis=1)
    # y = y[index]
    # x1 = x1[index]
    # x2 = x2[index]
    # x = x[index, :]

    # index = np.all(y > 1200, axis=1)
    # y = y[index]
    # x1 = x1[index]
    # x2 = x2[index]
    # x = x[index, :]
    # x = pd.DataFrame(x)
    # y = pd.DataFrame(y)
    # ic(x.shape)
    # ic(y.shape)
    temp = np.array([])
    x = np.array([])
    y = np.array([])
    for yi in range(0, 90):
        for xi in range(0,120):
            temp = np.append(temp, TEMP[yi, xi])
            x = np.append(x, xi)
            y = np.append(y, yi)
    ic(temp.shape)
    ic(x.shape)
    ic(y.shape)
    index = temp > 1200
    ic(index)
    x1 = pd.DataFrame(x[index])
    x2 = pd.DataFrame(y[index])
    x = np.vstack([x[index], y[index]])
    x = pd.DataFrame(x.T)
    y = pd.DataFrame(temp[index])
    ic(temp.shape)
    ic(x.shape)
    ic(y.shape)



    from mpl_toolkits.mplot3d import Axes3D  #3Dplot
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig=plt.figure()
    ax=Axes3D(fig)

    ax.scatter3D(x1, x2, y)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("y")

    plt.show()

    from sklearn.linear_model import LinearRegression
    import numpy as np

    model_lr = LinearRegression()
    model_lr.fit(x, y)

    fig=plt.figure()
    ax=Axes3D(fig)

    ax.scatter3D(x1, x2, y)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("y")

    mesh_x1 = np.arange(x1.min()[0], x1.max()[0], (x1.max()[0]-x1.min()[0])/20)
    mesh_x2 = np.arange(x2.min()[0], x2.max()[0], (x2.max()[0]-x2.min()[0])/20)
    mesh_x1, mesh_x2 = np.meshgrid(mesh_x1, mesh_x2)
    mesh_y = model_lr.coef_[0][0] * mesh_x1 + model_lr.coef_[0][1] * mesh_x2 + model_lr.intercept_[0]
    ax.plot_wireframe(mesh_x1, mesh_x2, mesh_y)
    plt.show()

    print(model_lr.coef_)
    print(model_lr.intercept_)
    print(model_lr.score(x, y))
    # [[ 4.20967798 13.28514945]]
    # [11.59918943]
    # 0.4754266111991394
