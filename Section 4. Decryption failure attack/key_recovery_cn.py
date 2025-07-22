import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams['font.family'] = 'SimSun'
plt.rcParams['font.size'] = 22


# PLOT the relation of num of ineqs and recovered coes
def coe_ine_512():
    ine_Bay = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000]
    coe_Bay = [141, 342.9, 433.2, 490.8, 536.8, 567.1, 604.9, 626.9, 660.1, 676.6, 701.5, 723.8, 739.2, 757.1, 774.4, 785.3, 796.9, 812.4, 827.5, 835.6, 842, 962, 998, 1012, 1019, 1022, 1023, 1023, 1023, 1023, 1023, 1024, 1024, 1024, 1024, 1024]

    ine_maj = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950,
               1000, 2000, 3000, 4000, 5000, 6000]
    coe_maj = [70, 214.1, 245.3, 273, 293.8, 313.3, 331.3, 338.4, 350.7, 362.1, 384, 390.1, 411.4, 420.4, 430.6, 443.9, 448.9, 456, 461.8, 466.9,
               471.4, 507, 511.9, 512, 512, 512]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_Bay, coe_Bay, kind='cubic')
    f2 = interp1d(ine_maj, coe_maj, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(1, 16000, 16000)
    xnew2 = np.linspace(1, 6000, 6000)

    fig, ax = plt.subplots(figsize=(10, 6))
    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1100)
    plt.xlim(-500, 16000)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='black', linestyle='-', label='概率方法[25]')
    plt.plot(xnew2, f2(xnew2), '-', color='black', linestyle='--', label='多数投票')

    # 添加y=1024的红色横线
    plt.axhline(y=1026, color='black', linestyle=':')
    plt.plot([-500, 6000], [514, 514], color='black', linestyle=':')
    plt.plot([3000, 3000], [0, 512], color='black', linestyle=':')
    plt.plot([13000, 13000], [0, 1024], color='black', linestyle=':')

    # plt.axvline(x=3000, ymin=0, ymax=512, color='b', linestyle='--', label='x = 3000')

    # 在图中添加标注
    plt.text(1, 1026, 'y = 1024', color='black', verticalalignment='bottom', fontsize=14)
    plt.text(1, 514, 'y = 512', color='black', verticalalignment='bottom', fontsize=14)

    # 添加坐标轴标签
    plt.xlabel('解密失败数量')
    plt.ylabel('私钥系数恢复数量')

    plt.legend()

    plt.tight_layout(pad=0.5)
    plt.show()


if __name__ == '__main__':
    # the relation of num of ineqs and recovered coes
    coe_ine_512()




