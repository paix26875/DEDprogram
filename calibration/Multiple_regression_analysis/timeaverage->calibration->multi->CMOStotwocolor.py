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
from icecream import ic

# numpyの配列表示数の設定
np.set_printoptions(threshold=np.inf)

def timeAverage(laser_power, middle_frame_number, frames):
    """
    二色温度計画像を時間平均する

    Parameters
    ----------
    laser_power : int
        レーザ出力
    begin_frame_number : int
        平均するフレームの開始点
    end_frame_number : int
        平均するフレームの終了点

    Returns
    -------
    TEMP : numpyの二次元配列
        二色温度計の時間平均値
    """
    # pathの設定
    total_frame_number = frames + 1
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
        begin_frame_number = middle_frame_number - int(frames/2)
        end_frame_number = middle_frame_number + int(frames/2)
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
    
    return TEMP

def calibration(fg, TEMP, haszero, average, samplenumber, dir_name, mid_frames, laser_power=1600, RGBmin=25, RGBmax=255):
    """
    二色温度計画像とCMOSカメラ画像の比較をする
    その結果をcsvファイルに出力する

    Parameters
    ----------
    laser_power : int
        レーザ出力
    fg : string
        フィルタとゲインの組み合わせ
    TEMP : numpyの二次元配列
        二色温度計の時間平均値
    haszero : bool
        温度とRGBの対応データに0を含めるかどうか
    average : int
        平均する温度範囲
    samplenumber : int
        データとして扱うサンプルの数の閾値
    dir_name : str
        溶融地画像があるディレクトリ
    mid_frames : numpy
        溶融地の真ん中のフレーム

    Returns
    -------
    csv_path : string
        結果を出力したcsvファイルの絶対パス
    """
    height, width = TEMP.shape
    # キャリブレーション
    mid_frame = mid_frames[int((laser_power-1400)/100)]
    img_CMOS = np.array(Image.open(dir_name + str(laser_power) + '/img_' + str(mid_frame) + '.bmp'))
        
    x,y = gp.get_gravitypoint_CMOS(img_CMOS, show_gp_img = False, print_gp = False)
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

    for temp in range (int(min(TEMP)),int(max(TEMP))+1,5):
        sum_g = 0
        sum_r = 0
        sum_b = 0
        n_r = 0
        n_g = 0
        n_b = 0
        # for i in range ((height-1)*(width-1)):
        # for i in range (height+width-1):
        for i in range (TEMP.size-1):
            # if TEMP[i] !=0 and CMOS_r[i] > RGBmin:
            #     if TEMP[i]<temp+average and TEMP[i]>temp-average:
            #         sum_r += CMOS_r[i]
            #         n_r += 1
            # if TEMP[i] !=0 and CMOS_g[i] > RGBmin:
            #     if TEMP[i]<temp+average and TEMP[i]>temp-average:
            #         sum_g += CMOS_g[i]
            #         n_g += 1
            # if TEMP[i] !=0 and CMOS_b[i] > RGBmin:
            #     if TEMP[i]<temp+average and TEMP[i]>temp-average:
            #         sum_b += CMOS_b[i]
            #         n_b += 1
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
    if haszero:
        df = df[(df.R != 0) | (df.G != 0) | (df.B != 0)]# RGBの全てが0なら削除
    else:
        df = df[(df.R != 0) & (df.G != 0) & (df.B != 0)]# RGBのどれか1つが0なら削除
    # df = df[df.temperature > 1900]
    # df = df[df.temperature < 2400]
    # print(df)


    csv_path = '/Users/paix/Desktop/Python_lab/frame_data/20210706/csv/' + fg + '/' + str(laser_power) + 'to_csv_out_out.csv'
    df.to_csv(csv_path)

    return csv_path

def multipleLinearRegressionAnalysis(csv_path, summary=False):
    """
    温度とRGBのデータについて重回帰分析を行う

    Parameters
    ----------
    csv_path : string
        結果を出力したcsvファイルの絶対パス
    summary : bool
        重回帰分析の結果をまとめた表を出力するかどうか
    
    Returns
    -------
    coefs : numpy
        重回帰式の係数
    """
    # # 3つ目
    df = pd.read_csv(csv_path, sep=',')
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

    from sklearn.linear_model import LinearRegression

    model_lr = LinearRegression()
    model_lr.fit(x, y)

    if summary:
        from sklearn import preprocessing

        sscaler = preprocessing.StandardScaler()
        sscaler.fit(x)
        xss_sk = sscaler.transform(x) 
        sscaler.fit(y)
        yss_sk = sscaler.transform(y)
        import statsmodels.api as sm
        x_add_const = sm.add_constant(xss_sk)
        model_sm = sm.OLS(yss_sk, x_add_const).fit()
        print(model_sm.summary())
    ic(model_lr.score(x, y))
    coefs = np.array([model_lr.coef_[0][0], model_lr.coef_[0][1], model_lr.coef_[0][2], model_lr.intercept_[0]])

    return coefs

def CMOStoTwoColor(laser_power, fg, coefs, save_path, threshold = 20):
    """
    CMOSカメラ画像→温度配列→二色温度計画像

    Parameters
    ----------
    laser_power : int
        レーザ出力
    fg : string
        フィルタとゲインの組み合わせ
    coefs : numpy
        重回帰式の係数
    save_path : string
        保存する画像の絶対パス
    Returns
    -------
    """
    height = 300
    width = 300
    if fg == 'f4-g16':
        dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g16/"
        mid_frames = [28, 41, 31, 39, 36]
    elif fg == 'f4-g24':
        dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g24/"
        mid_frames = [32, 38, 32, 26, 57]
    mid_frame = mid_frames[int((laser_power-1400)/100)]
    img_CMOS = np.array(Image.open(dir_name + str(laser_power) + '/img_' + str(mid_frame) + '.bmp'))
    
    x,y = gp.get_gravitypoint_CMOS(img_CMOS, show_gp_img = False, print_gp = False)
    trimmed_img_r = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 0]
    trimmed_img_g = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 1]
    trimmed_img_b = img_CMOS[ y - int(height/2) : y + int(height/2) , x - int(width/2) : x + int(width/2), 2]
    
    img_zero = np.zeros(height*width)
    
    
    img_red = trimmed_img_r[:,:].reshape(height*width)
    ret, img_thresh = cv2.threshold(img_red, threshold, 255, cv2.THRESH_BINARY)
    trimmed_img_r = trimmed_img_r.reshape(height*width)
    trimmed_img_g = trimmed_img_g.reshape(height*width)
    trimmed_img_b = trimmed_img_b.reshape(height*width)
    for i in img_thresh.nonzero():
        img_zero[i] += trimmed_img_r[i]*coefs[0] + trimmed_img_g[i]*coefs[1] + trimmed_img_b[i]*coefs[2] + coefs[3]
    # ic(img_zero)
    twocolor_CMOS = tc.tocolor(img_zero, height, width).reshape(height, width, 3)
    # ic(twocolor_CMOS)
    img_ave = np.array(twocolor_CMOS, dtype=np.int8)
    pil_img = Image.fromarray(img_ave, mode="RGB")
    # save_name = str(laser_power) + '_' + str(gain) + '_' + str(average) + '_' + nonzero + "_RGB" + ".bmp"
    pil_img.save(save_path)
    # pil_img.save('/Users/paix/Desktop/Python_lab/calibration/Multiple_regression_analysis/data/temp/CMOS_raw_int8_RGBmin' + str(average) + afbf + str(threshold) + save_name)


if __name__ == '__main__':
    # レーザ出力とフレーム数の設定
    frames = 200
    middle_frame_numbers = [4605, 4608, 4645, 4641, 4666]
    laser_power = 1600
    average = 10
    samplenumber = 5
    for fg in ['f4-g16', 'f4-g24']:
        # for fg in ['f4-g24']:
        # for average in range(10, 60, 10):
        for average in range(10, 20, 10):
            # for haszero in [True, False]:
            for haszero in [True]:
                # for samplenumber in range(1,6):
                for samplenumber in range(5,6):
                    middle_frame_number = middle_frame_numbers[int((laser_power - 1400) / 100)]
                    if haszero:
                        zero = 'haszero'
                    else:
                        zero = 'nonzero'
                    RGBvalue = 0
                    height = 90
                    width = 120
                    if fg == 'f4-g16':
                        dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g16/"
                        mid_frames = [28, 41, 31, 39, 35]
                        RGBmin = 17
                    elif fg == 'f4-g24':
                        dir_name = "/Users/paix/Desktop/Python_lab/frame_data/20210706/after_projection/f4-g24/"
                        mid_frames = [32, 38, 32, 26, 56]
                        RGBmin = 18
                    RGBmax = 255

                    TEMP = timeAverage(laser_power, middle_frame_number, frames)
                    csv_path = calibration(fg, TEMP, haszero, average, samplenumber, dir_name, mid_frames, laser_power=laser_power, RGBmin=RGBmin)
                    coefs = multipleLinearRegressionAnalysis(csv_path, summary=True)
                    ic(coefs)
                    for laserpower in range(1400, 1900, 100):
                        save_name = str(laserpower) + '_' + str(fg) + '_' + str(average) + '_' + zero + '_' + str(samplenumber) + "_RGB" + ".bmp"
                        save_dir = '/Users/paix/Desktop/Python_lab/frame_data/20210719/CMOSTemperatureImage/tempMax2400RGBmin' + str(RGBmin) + 'frames' + str(frames) + 'callaser' + str(laser_power) + '/'
                        os.makedirs(save_dir, exist_ok=True)
                        save_path = save_dir + save_name
                        CMOStoTwoColor(laserpower, fg, coefs, save_path, threshold=RGBmin)
