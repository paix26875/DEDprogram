import cv2
from PIL import Image
import numpy as np
from icecream import ic
import gravitypoint as gp
import trimming as tr
import twocolor_convert as tc
from matplotlib import pyplot as plt
import os


# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)



if __name__ == '__main__':

    # レーザ出力とフレーム数の設定
    laser_power = 1600
    frames = 100
    begin_frame_number = 4695
    end_frame_number = begin_frame_number + frames
    RGBvalue = 0
    height = 90
    width = 120
    RGBmin = 25
    RGBmax = 255

    # pathの設定
    total_frame_number = end_frame_number - begin_frame_number + 1
    directory_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/pyro/"
    base_name = directory_name + str(laser_power) + "/" + str(laser_power) + "0OUT"
    os.makedirs('calibration/time_average/colorimg/20210706/', exist_ok=True)
    color_img_path = 'calibration/time_average/colorimg/20210706/' + str(laser_power) + "_" + str(total_frame_number) + ".bmp"
    if os.path.exists(color_img_path):
    # if False:
        img_pil = Image.open(color_img_path)
        img_np = np.array(img_pil)
        temperature_ave = tc.totemperature(img_np)
        TEMP = temperature_ave# 1次元配列
        TEMPplt = temperature_ave.reshape(90*120)# 2次元配列
        # # 温度ヒストグラム表示
        plt.hist(TEMPplt, color="red", bins=128)
        plt.ylim(0, 200)
        plt.xlim(1300, 3000)
        plt.xlabel("temperature")
        plt.show()
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
            ic(frame_number)
            # 1枚ずつ重心周りでトリミングしていく
            img_pil = Image.open(base_name + str(frame_number) + ".BMP")
            img_np = np.array(img_pil)
            rough_trimmed_img = tr.img_trimming(img_np, 220, 310, 640, 1279)
            x, y = gp.get_gravitypoint_img(rough_trimmed_img, False)# うまくいった
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
        pil_img.save('calibration/time_average/colorimg/20210706/' + save_name)
    # 温度の時間平均算出終了




    # キャリブレーション
    # 20210421
    # dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210421/CMOS/after_projection/"
    # if laser_power == 1400:
    #     img_CMOS = np.array(Image.open(dir_name + '1400/img_72.bmp'))
    # elif laser_power == 1600:
    #     img_CMOS = np.array(Image.open(dir_name + '1600/img_86.bmp'))
    # elif laser_power == 1800:
    #     img_CMOS = np.array(Image.open(dir_name + '1800/img_95.bmp'))
    # 20210706
    dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g16/"
    if laser_power == 1400:
        img_CMOS = np.array(Image.open(dir_name + '1400/img_72.bmp'))
    elif laser_power == 1600:
        img_CMOS = np.array(Image.open(dir_name + '1600/img_31.bmp'))
    elif laser_power == 1800:
        img_CMOS = np.array(Image.open(dir_name + '1800/img_95.bmp'))
        
    x,y = gp.get_gravitypoint_CMOS(img_CMOS)
    trimmed_img = img_CMOS[ y - 45 : y + 45 , x - 60 : x + 60]
    # CMOS_r = trimmed_img[:, :, 0]
    # CMOS_g = trimmed_img[:, :, 1]
    # CMOS_b = trimmed_img[:, :, 2]

    CMOS = trimmed_img[:, :, RGBvalue]


    x = np.reshape(CMOS, height * width)
    y = np.reshape(TEMP, height * width)

    # キャリブレーションをまとめる変数の定義
    xnew = np.arange(RGBmin,RGBmax,5)# RGB値（横軸）
    ynew = np.zeros(13)# RGBに対応する温度（縦軸）
    nnew = np.zeros(13)# サンプル数（第2縦軸）
    
    # RGBに対応する温度をynewに格納していく
    # その時のサンプル数をnnewに格納していく
    for R in range (RGBmin,RGBmax,5):
        sum=0
        n=0
        for i in range ((height-1)*(width-1)):
            if y[i] !=0 and x[i] !=0:
                if x[i]<R+3 and x[i]>R-2:
                    sum += y[i]
                    n += 1
        if n != 0:
            ynew = np.append(ynew,sum/n)
            nnew = np.append(nnew, n)
        else:
            ynew = np.append(ynew,0)
            nnew = np.append(nnew,0)
    ynew = ynew[13:]
    nnew = nnew[13:]
    
    # グラフに表示するためにデータを整形していく
    # 非ゼロ要素の抽出 
    # ゼロ要素を含むと表示が小さくなったり近似する時に邪魔なので取り除く 
    result_rgb = xnew[ynew.nonzero()]
    result_temperature = ynew[ynew.nonzero()]
    result_samplenumber = nnew[ynew.nonzero()]
    
    xnew = result_rgb
    ynew = result_temperature
    nnew = result_samplenumber

    # 一次近似
    a,b = np.polyfit(xnew, ynew, 1)
    yfit = a*xnew + b
    
    # 決定係数の算出
    yave = np.mean(ynew)#平均値
    sum_all = 0
    sum_fit = 0
    for i in range(ynew.size):
        sum_all += (ynew[i] - yave)**2
        sum_fit += (yfit[i] - yave)**2
    R2 = sum_fit/sum_all

    ic(RGBvalue)
    ic(round(R2, 3))


    if RGBvalue == 0:
        RGB = "R"
    elif RGBvalue == 1:
        RGB = "G"
    elif RGBvalue == 2:
        RGB = "B"
    
    formula = "T = " + str(round(a,2)) + RGB + "+" + str(round(b,2))
    ic(formula)

    ###########
    #結果の表示#
    ##########


    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

    # figureオブジェクトを作成
    fig = plt.figure()
    # fig = plt.figure(tight_layout=False)
    ax1 = fig.subplots(subplot_kw=dict(ymargin=0.3, xlabel=RGB, ylabel='温度[℃]'))

    # ax1とax2を関連させる
    # ax2 = ax1.twinx()
    
    # それぞれのaxesオブジェクトのlines属性にLine2Dオブジェクトを追加
    # ax1.plot(xnew, ynew, marker='.', color='blue', label="溶融池温度", linestyle='None')
    # ax1.plot(xnew, yfit, color='orange', label="一次近似")
    ax1.plot(xnew, ynew, marker='.', color='blue', label="キャリブレーション値", linestyle='None')
    ax1.plot(xnew, yfit, color='orange', label="1次近似直線")
    # ax2.plot(xnew, nnew, marker='.', color='red', label="サンプル数", linestyle='None')
    
    # ax1.text(RGBmin, 2150, "R2 = " + str(round(R2, 3)), size=10)
    # ax1.text(RGBmin, 2120, formula, size=10)
    # ax1.text(RGBmin, 2090, "平均フレーム数：" + str(frames), size=10)
    # ax1.text(RGBmin, 2060, "RGBの最小値：" + str(RGBmin), size=10)
    ax1.text(RGBmin, 2170, "R2 = " + str(round(R2, 3)), size=10)
    ax1.text(RGBmin, 2150, formula, size=10)
    ax1.text(RGBmin, 2130, "平均フレーム数：" + str(frames), size=10)
    ax1.text(RGBmin, 2110, "RGBの最小値：" + str(RGBmin), size=10)

    

    #凡例をつける
    ax1.legend()
    # ax2.legend()
    # # 結果のプロット
    # plt.plot(xnew, ynew, 'o')
    # plt.plot(xnew, nnew, 'o')

    
    plt.show()
