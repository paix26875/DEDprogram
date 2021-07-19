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
import csv

# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)



if __name__ == '__main__':
    print('フィルターとゲインを選択： 16 / 24')
    g = input()
    fg = 'f4-g' + g
    # レーザ出力とフレーム数の設定
    frames = 100
    laser_power = 1600
    average = 10
    samplenumber = 5
    nonzero = 'haszero'
    for fg in ['f4-g16', 'f4-g24']:
        for average in range(10, 60, 10):
            for nonzero in ['nonzero', 'haszero']:
                if laser_power == 1400:
                    begin_frame_number = 4605
                if laser_power == 1500:
                    begin_frame_number = 4608
                if laser_power == 1600:
                    begin_frame_number = 4645
                if laser_power == 1700:
                    begin_frame_number = 4641
                if laser_power == 1800:
                    begin_frame_number = 4666

                end_frame_number = begin_frame_number + frames
                RGBvalue = 0
                height = 90
                width = 120
                RGBmin = 25
                RGBmax = 255

                # pathの設定
                total_frame_number = end_frame_number - begin_frame_number + 1
                directory_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/pyrometer_short/"
                base_name = directory_name + str(laser_power) + "/" + str(laser_power) + "0OUT"
                os.makedirs('frame_data/20210706/colorimg/', exist_ok=True)
                color_img_path = 'frame_data/20210706/colorimg/' + str(laser_power) + "_" + str(total_frame_number) + ".bmp"
                if os.path.exists(color_img_path):
                # if False:
                    img_pil = Image.open(color_img_path)
                    img_np = np.array(img_pil)
                    temperature_ave = tc.totemperature(img_np)
                    TEMP = temperature_ave# 1次元配列
                    TEMPplt = temperature_ave.reshape(90*120)# 2次元配列
                    # # 温度ヒストグラム表示
                    # plt.hist(TEMPplt, color="red", bins=128)
                    # plt.ylim(0, 200)
                    # plt.xlim(1300, 3000)
                    # plt.xlabel("temperature")
                    # plt.show()
                else:
                # 温度の時間平均算出開始
                    # 1枚目の溶融池画像を格納
                    img_pil = Image.open(base_name + str(begin_frame_number) + ".BMP")
                    img_np = np.array(img_pil)
                    rough_trimmed_img = tr.img_trimming(img_np, 240, 330, 640, 1279)
                    x, y = gp.get_gravitypoint_img(rough_trimmed_img)
                    trimmed_img = rough_trimmed_img[ : , x - 60 : x + 60]
                    # 温度データに変換 ######
                    temperature_sum = tc.totemperature(trimmed_img)

                    for frame_number in range(begin_frame_number + 1, end_frame_number + 1):
                        ic(frame_number)
                        # 1枚ずつ重心周りでトリミングしていく
                        img_pil = Image.open(base_name + str(frame_number) + ".BMP")
                        img_np = np.array(img_pil)
                        rough_trimmed_img = tr.img_trimming(img_np, 240, 330, 640, 1279)
                        x, y = gp.get_gravitypoint_img(rough_trimmed_img, False)# うまくいった
                        # trimmed_img = rough_trimmed_img[ : , x - 60 : x + 60]
                        trimmed_img = img_np[240 + y - 45 : 240 + y + 45, 640 + x - 60 : 640 + x + 60]
                        
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
                    pil_img.save('frame_data/20210706/colorimg/' + save_name)
                    # pil_img.save('calibration/time_average/colorimg/20210421/' + save_name)
                # 温度の時間平均算出終了




                # キャリブレーション
                if fg == 'f4-g16':
                    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g16/"
                    mid_frames = [28, 41, 31, 39, 36]
                elif fg == 'f4-g24':
                    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g24/"
                    mid_frames = [32, 38, 32, 26, 57]
                mid_frame = mid_frames[int((laser_power-1400)/100)]
                img_CMOS = np.array(Image.open(dir_name + str(laser_power) + '/img_' + str(mid_frame) + '.bmp'))
                    
                x,y = gp.get_gravitypoint_CMOS(img_CMOS, show_gp_img = False)
                trimmed_img = img_CMOS[ y - 45 : y + 45 , x - 60 : x + 60]
                # import cv2
                # cv2.imshow('img', trimmed_img)
                # cv2.waitKey(0)
                CMOS_r = trimmed_img[:, :, 0]
                CMOS_g = trimmed_img[:, :, 1]
                CMOS_b = trimmed_img[:, :, 2]

                # CMOS = trimmed_img[:, :, RGBvalue]
                TEMP = TEMP.reshape(90*120)
                CMOS_r = CMOS_r.reshape(90*120)[np.nonzero(TEMP)]
                CMOS_g = CMOS_g.reshape(90*120)[np.nonzero(TEMP)]
                CMOS_b = CMOS_b.reshape(90*120)[np.nonzero(TEMP)]
                TEMP = TEMP.reshape(90*120)[np.nonzero(TEMP)]

                CMOS_r_new = np.array([])
                CMOS_g_new = np.array([])
                CMOS_b_new = np.array([])
                TEMP_new = np.arange(int(min(TEMP)),int(max(TEMP))+1,5)

                ic(TEMP.shape)


                for temp in range (int(min(TEMP)),int(max(TEMP))+1,5):
                    sum_g = 0
                    sum_r = 0
                    sum_b = 0
                    n_r = 0
                    n_g = 0
                    n_b = 0
                    # for i in range ((height-1)*(width-1)):
                    # for i in range (height+width-1):
                    for i in range (height+width-1):
                        if TEMP[i] !=0 and CMOS_r[i] > RGBmin:
                            if TEMP[i]<temp+average and TEMP[i]>temp-average:
                                sum_r += CMOS_r[i]
                                n_r += 1
                        if TEMP[i] !=0 and CMOS_g[i] > RGBmin:
                            if TEMP[i]<temp+average and TEMP[i]>temp-average:
                                sum_g += CMOS_g[i]
                                n_g += 1
                        if TEMP[i] !=0 and CMOS_b[i] > RGBmin:
                            if TEMP[i]<temp+average and TEMP[i]>temp-average:
                                sum_b += CMOS_b[i]
                                n_b += 1

                    if n_r > samplenumber:
                        CMOS_r_new = np.append(CMOS_r_new, sum_r/n_r)
                    else:
                        CMOS_r_new = np.append(CMOS_r_new, 0)
                    if n_g > samplenumber:
                        CMOS_g_new = np.append(CMOS_g_new, sum_g/n_g)
                    else:
                        CMOS_g_new = np.append(CMOS_g_new, 0)
                    if n_b > samplenumber:
                        CMOS_b_new = np.append(CMOS_b_new, sum_b/n_b)
                    else:
                        CMOS_b_new = np.append(CMOS_b_new, 0)
                        # xnew = np.append(xnew,sum/n)
                        # nnew = np.append(nnew, n)
                        # xnew = np.append(xnew,0)
                        # nnew = np.append(nnew,0)

                data = np.vstack([TEMP_new, CMOS_r_new, CMOS_g_new, CMOS_b_new]).T
                # ic(data)
                np.savetxt('/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + '.csv', data, delimiter=',', fmt='%d')
                header = ["temperature","R","G","B"]
                with open('/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + 'to_csv_out.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    with open('/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + '.csv') as fr:
                        reader = csv.reader(fr)
                        writer.writerows(reader)

                    
                # ヘッダーに "temperature","R","G","B" を追加
                # 2つ目
                df = pd.read_csv('/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + 'to_csv_out.csv', sep=',')
                if nonzero == 'haszero':
                    df = df[(df.R != 0) | (df.G != 0) | (df.B != 0)]# RGBの全てが0なら削除
                elif nonzero == 'nonzero':
                    df = df[(df.R != 0) & (df.G != 0) & (df.B != 0)]# RGBのどれか1つが0なら削除
                # print(df)

                df.to_csv('/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + 'to_csv_out_out.csv')

                # # 3つ目
                df = pd.read_csv('/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + 'to_csv_out_out.csv', sep=',')
                df.head()
                x = df[['R', 'G', 'B']]
                y = df[['temperature']]
                x1 = df[['R']]
                x2 = df[['G']]
                x3 = df[['B']]
                # ic(x.shape)
                # ic(y.shape)
                x = x.values
                y = y.values
                # index = np.all(x > 20, axis=1)
                # y = y[index]
                # x1 = x1[index]
                # x2 = x2[index]
                # x3 = x3[index]
                # x = x[index, :]

                index = np.all(y > 1200, axis=1)
                y = y[index]
                x1 = x1[index]
                x2 = x2[index]
                x3 = x3[index]
                x = x[index, :]
                x = pd.DataFrame(x)
                y = pd.DataFrame(y)
                # ic(x.shape)
                # ic(y.shape)




                # from mpl_toolkits.mplot3d import Axes3D  #3Dplot
                # import matplotlib.pyplot as plt
                # import seaborn as sns

                # fig=plt.figure()
                # ax=Axes3D(fig)

                # ax.scatter3D(x1, x2, y)
                # ax.set_xlabel("x1")
                # ax.set_ylabel("x2")
                # ax.set_zlabel("y")

                # plt.show()

                from sklearn.linear_model import LinearRegression
                import numpy as np

                model_lr = LinearRegression()
                model_lr.fit(x, y)

                # fig=plt.figure()
                # ax=Axes3D(fig)

                # ax.scatter3D(x1, x2, y)
                # ax.set_xlabel("x1")
                # ax.set_ylabel("x2")
                # ax.set_zlabel("y")

                # mesh_x1 = np.arange(x1.min()[0], x1.max()[0], (x1.max()[0]-x1.min()[0])/20)
                # mesh_x2 = np.arange(x2.min()[0], x2.max()[0], (x2.max()[0]-x2.min()[0])/20)
                # mesh_x1, mesh_x2 = np.meshgrid(mesh_x1, mesh_x2)
                # mesh_y = model_lr.coef_[0][0] * mesh_x1 + model_lr.coef_[0][1] * mesh_x2 + model_lr.intercept_[0]
                # ax.plot_wireframe(mesh_x1, mesh_x2, mesh_y)
                # plt.show()

                ic(model_lr.coef_[0][0])
                ic(model_lr.coef_[0][1])
                ic(model_lr.coef_[0][2])
                ic(model_lr.intercept_)
                ic(model_lr.score(x, y))
                # [[ 4.20967798 13.28514945]]
                # [11.59918943]
                # 0.4754266111991394

                from sklearn import preprocessing

                sscaler = preprocessing.StandardScaler()
                sscaler.fit(x)
                xss_sk = sscaler.transform(x) 
                sscaler.fit(y)
                yss_sk = sscaler.transform(y)

                # print(xss_sk)
                # print(yss_sk)

                import statsmodels.api as sm

                x_add_const = sm.add_constant(xss_sk)
                model_sm = sm.OLS(yss_sk, x_add_const).fit()
                # print(model_sm.summary())
