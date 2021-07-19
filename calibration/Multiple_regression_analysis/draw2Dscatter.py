import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d # scipyのモジュールを使う
from icecream import ic
import os

def make_func(in_x):
    np.random.seed(0)
    out_y = np.exp(-in_x) + 0.4*(np.random.rand(in_x.size) - 0.5) # exp(-x)の式にランダムな誤差を入れる
    return out_y

def spline_interp(in_x, in_y):
    out_x = np.linspace(np.min(in_x), np.max(in_x), np.size(in_x)*100) # もとのxの個数より多いxを用意
    func_spline = interp1d(in_x, in_y, kind='cubic') # cubicは3次のスプライン曲線
    out_y = func_spline(out_x) # func_splineはscipyオリジナルの型

    return out_x, out_y

def main(type, data):
    # 日本語表示の有効化
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']
    
    # 条件の入力
    print('which type? laser / feed / EFconstant')
    ic(type)
    # type = input()
    print('which data? peak / width / area')
    ic(data)
    # data = input()

    # x軸リスト
    laser_list = [1000, 1200, 1400, 1600, 1800, 2000]
    feed_list = [625, 750, 875, 1000, 1125, 1250]
    # EFconstant_list = ['1000-625', '1200-750', '1400-875', '1600-1000', '1800-1125', '2000-1250']
    EFconstant_list = [1000, 1200, 1400, 1600, 1800, 2000]
    
    # Figureの作成
    fig = plt.figure()
    ax = fig.subplots()

    # xの設定とx軸ラベル・タイトルの設定
    if type == 'laser':
        x1 = laser_list
        ax.set_xlabel("レーザ出力 [W]")
        title = "レーザ出力と" + data + "の関係"
        

    elif type == 'feed':
        x1 = feed_list
        ax.set_xlabel("レーザ走査速度 [mm/min]")
        title = "レーザ走査速度と" + data + "の関係"

    elif type == 'EFconstant':
        x1 = EFconstant_list
        ax.set_xlabel("レーザ出力 [W]/レーザ走査速度 [mm/min]")
        title = "入力エネルギ密度一定の時の" + data

    if data == 'peak':
        ax.set_ylim(2000, 2500)
    elif data == 'width':
        ax.set_ylim(100, 250)
    elif data == 'area':
        ax.set_ylim(5000, 20000)
    
    # y軸データの読み込みとy軸ラベルの設定
    fname = '/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/csv/' + type + '_' + data + '.csv'
    ax.set_ylabel(data)
    y1 = np.loadtxt(fname, delimiter=',')

    # スプライン補間
    x2, y2 = spline_interp(x1, y1)

    
    ax.scatter(x1, y1, linestyle='solid', color="red") # 点の描画
    ax.plot(x2, y2, color='red', label='spline', alpha=0.7) # スプライン補間曲線の描画
    fig.text(0.30, 0, title, fontsize=12)
    ax.legend()
    # plt.show()
    os.makedirs('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/2D/', exist_ok=True)
    fig.savefig('/Users/paix/Documents/Research/M2打ち合わせ/第6回打ち合わせ資料/2D/' + type + '_' + data + '.png')

if __name__ == '__main__':
    for type in ['laser', 'feed', 'EFconstant']:
        for data in ['peak', 'width', 'area']:
            main(type, data)