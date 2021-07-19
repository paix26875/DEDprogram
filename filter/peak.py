'''
for文（ファイル数）
    numpyで画像読み出し
    np.max# ピークRGB
    RGBヒストグラム




'''
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    print("filter:")
    # filternum = input()
    # filter = '83'
    filters = (["f4g8", "f4g32", "f5g32", "f5g64"])
    print("laser power:")
    # laser_power = input()
    laser_powers = (["1200", "1600", "2000"])
    print("layer:")
    # layer = input()
    layers = (["1", "5", "11"])
    # for filter, laser_power, layer in zip(filters, laser_powers, layers):
    for filter in filters:
        for laser_power in laser_powers:
            for layer in layers:
                path = "/Users/paix/Desktop/Python_lab/frame_data/20210629/" + filter + "/" + laser_power + '_' + layer + "/"
                print(path)
                files = os.listdir(path)  
                count = len(files)  
                print(count)

                R = np.array([])
                G = np.array([])
                B = np.array([])

                for i in range(0,count):
                    img = np.array(Image.open(path + "img_" + str(i) + ".bmp"))
                    R = np.append(R, np.max(img[:,:,0]))
                    G = np.append(G, np.max(img[:,:,1]))
                    B = np.append(B, np.max(img[:,:,2]))

                
                # 日本語表示の有効化
                from matplotlib import rcParams
                rcParams['font.family'] = 'sans-serif'
                rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']
                
                fig = plt.figure()
                ax = fig.subplots()

                ax.set_xlabel("フレーム", fontsize = 12)
                ax.set_ylabel("ピークRGB", fontsize = 12)
                
                x = np.arange(0,count)
                ax.plot(x, R, '-',  label = "red", color="red", alpha=0.6)
                ax.plot(x, G, '-',  label = "green", color="green", alpha=0.6)
                ax.plot(x, B, '-',  label = "blue", color="blue", alpha=0.6)

                ax.legend()
                fig.subplots_adjust(bottom=0.2)
                title = 'フィルタ：' + filter + '/レーザ出力：' + str(laser_power) + ' W/' + layer + '層目'
                fig.text(0.20, 0.02, title, fontsize=14)
                # plt.show()
                os.makedirs("/Users/paix/Documents/Research/M2打ち合わせ/第7回打ち合わせ資料/peak/" + filter + "/" + str(laser_power) + '_' + layer , exist_ok=True)
                fig.savefig("/Users/paix/Documents/Research/M2打ち合わせ/第7回打ち合わせ資料/peak/" + filter + "/" + str(laser_power) + '_' + layer + ".png")
                plt.close
