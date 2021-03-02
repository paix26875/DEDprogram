from matplotlib import pyplot as plt
import numpy as np

def draw_graph(y, t):
    # グラフの描画
    plt.plot(t, y)
    plt.show()

if __name__ == "__main__":
    t=np.arange(0, 10, 0.1)
    y=np.sin(t)
    draw_graph(y, t)
    