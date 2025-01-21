import numpy as np
import math
import matplotlib.pyplot as plt
import itertools
from scipy.interpolate import interp1d
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16



# the relation of num of ineqs and recovered coes
def coe_ine():
    ine_ARV = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000]
    coe_ARV = [141, 370.3, 468.1, 533.7, 577.9, 611.7, 642.2, 660.2, 695.8, 717.7, 739.8, 740.3, 752.3, 762.9, 774.4, 784.2, 795.2, 801.9, 807.5, 813.4, 822.0, 886.1, 925.7, 939.3, 949.6, 955.3, 958.6, 966.7, 971.8, 972.5, 970.5, 974.9, 976.9, 976.2, 979.0, 977.5, 981.1, 980.7, 979.9, 981.0, 981.6, 981.8, 983.0, 981.6, 982.5, 982.1]
    ine_ARV_s = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    coe_ARV_s = [141, 370.3, 468.1, 533.7, 577.9, 611.7, 642.2, 660.2, 695.8, 717.7, 739.8, 740.3, 752.3, 762.9, 774.4, 784.2, 795.2, 801.9, 807.5, 813.4, 822.0, 886.1, 925.7, 939.3, 949.6, 955.3, 958.6, 966.7, 971.8, 972.5, 970.5, 974.9]

    ine_Bay = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000]
    coe_Bay = [141, 342.9, 433.2, 490.8, 536.8, 567.1, 604.9, 626.9, 660.1, 676.6, 701.5, 723.8, 739.2, 757.1, 774.4, 785.3, 796.9, 812.4, 827.5, 835.6, 842, 962, 998, 1012, 1019, 1022, 1023, 1023, 1023, 1023, 1023, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
    ine_Bay_s = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    coe_Bay_s = [141, 342.9, 433.2, 490.8, 536.8, 567.1, 604.9, 626.9, 660.1, 676.6, 701.5, 723.8, 739.2, 757.1, 774.4, 785.3, 796.9, 812.4, 827.5, 835.6, 842, 962, 998, 1012, 1019, 1022, 1023, 1023, 1023, 1023, 1023, 1024]

    ine_maj = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000,
               2000, 3000, 4000, 5000]
    coe_maj = [70, 214.1, 245.3, 273, 293.8, 313.3, 331.3, 338.4, 350.7, 362.1, 384, 390.1, 411.4, 420.4, 430.6, 443.9, 448.9, 456, 461.8, 466.9,
               471.4, 507, 511.9, 512, 512, 512]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_ARV, coe_ARV, kind='cubic')
    f2 = interp1d(ine_Bay, coe_Bay, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew = np.linspace(1, 15000, 15000)

    # 绘制原始数据点
    # plt.plot(ine_ARV, coe_ARV, 'o', label='Data 1')
    # plt.plot(ine_Bay, coe_Bay, 'o', label='Data 2')

    # 绘制平滑曲线
    plt.plot(xnew, f1(xnew), '-', label='Result in [22]')
    plt.plot(xnew, f2(xnew), '-', label='Result 1')

    # 添加y=1024的红色横线
    plt.axhline(y=1025, color='r', linestyle='--')
    # 添加x=12000的蓝色竖线
    plt.axvline(x=13000, color='b', linestyle='--')

    # 在图中添加标注
    plt.text(1, 1025, 'y = 1024', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.xlabel('number of failures')
    plt.ylabel('recovered coefficients')

    plt.legend()
    plt.show()


def coe_ine_512():
    ine_Bay = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000]
    coe_Bay = [141, 342.9, 433.2, 490.8, 536.8, 567.1, 604.9, 626.9, 660.1, 676.6, 701.5, 723.8, 739.2, 757.1, 774.4, 785.3, 796.9, 812.4, 827.5, 835.6, 842, 962, 998, 1012, 1019, 1022, 1023, 1023, 1023, 1023, 1023, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
    ine_Bay_s = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    coe_Bay_s = [141, 342.9, 433.2, 490.8, 536.8, 567.1, 604.9, 626.9, 660.1, 676.6, 701.5, 723.8, 739.2, 757.1, 774.4, 785.3, 796.9, 812.4, 827.5, 835.6, 842, 962, 998, 1012, 1019, 1022, 1023, 1023, 1023, 1023, 1023, 1024]

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

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1100)
    plt.xlim(-500, 16000)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Result 1')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Result 2')

    # 添加y=1024的红色横线
    plt.axhline(y=1026, color='r', linestyle='--')
    # 添加y=1024的红色横线
    # plt.axhline(y=514, color='r', linestyle='--', label='y = 512')
    # 添加x=12000的蓝色竖线
    # plt.axvline(x=10000, color='b', linestyle='--', label='x = 10000')

    plt.plot([-500, 6000], [514, 514], color='r', linestyle='--')

    plt.plot([3000, 3000], [0, 512], color='blue', linestyle='--')
    plt.plot([13000, 13000], [0, 1024], color='blue', linestyle='--')

    # plt.axvline(x=3000, ymin=0, ymax=512, color='b', linestyle='--', label='x = 3000')

    # 在图中添加标注
    plt.text(1, 1028, 'y = 1024', color='red', verticalalignment='bottom')
    plt.text(1, 516, 'y = 512', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.xlabel('number of failures')
    plt.ylabel('recovered coefficients')

    plt.legend(loc='lower right')
    plt.show()


def coe_ine_DRV20():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
               100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900]

    coe_DRV = [306, 423.1, 517.4, 597.3, 664.1, 717.4, 767.1, 816.1, 853.1, 894.6,
               924.2, 1165.7, 1304.0, 1377.4, 1432.8, 1465.0, 1486.1, 1500.0, 1511.1, 1519.8, 1525.9, 1528.7, 1530.6, 1531.8, 1532.6, 1534.2, 1534.5, 1535.3, 1535.6, 1535.1, 1535.5, 1535.7, 1536.0, 1535.6, 1535.9, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0]

    coe_DRV_s = [153, 207.7, 242.8, 284.8, 322.7, 340.7, 369.8, 393.0, 418.7, 442.7,
                 463.0, 623.8, 707.8, 742.2, 757.4, 764.8, 766.4, 767.3, 767.4, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')
    f2 = interp1d(ine_DRV, coe_DRV_s, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(1, 3000, 3000)
    xnew2 = np.linspace(1, 2000, 2000)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1700)
    plt.xlim(-200, 3300)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Result in [22]')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Result 3')

    # 添加y=1024的红色横线
    # plt.axhline(y=1538, color='r', linestyle='--')
    # 添加y=1024的红色横线
    # plt.axhline(y=514, color='r', linestyle='--', label='y = 512')
    # 添加x=12000的蓝色竖线
    # plt.axvline(x=10000, color='b', linestyle='--', label='x = 10000')

    plt.plot([-500, 3000], [1538, 1538], color='r', linestyle='--')
    plt.plot([-500, 2000], [770, 770], color='r', linestyle='--')

    plt.plot([1000, 1000], [0, 768], color='blue', linestyle='--')
    plt.plot([2600, 2600], [0, 1536], color='blue', linestyle='--')

    # plt.axvline(x=3000, ymin=0, ymax=512, color='b', linestyle='--', label='x = 3000')

    # 在图中添加标注
    plt.text(-100, 1538, 'y = 1536', color='red', verticalalignment='bottom')
    plt.text(-100, 770, 'y = 768', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.xlabel('num of failures')
    plt.ylabel('recovered coefficients')

    plt.legend()
    plt.show()


def coe_ine_DRV20_Kyber512():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490]
    coe_DRV = [300, 605.65, 745.42, 832.96, 887.6, 925.52, 954.07, 971.37, 985.16, 996.57, 1003.06, 1008.52, 1012.5, 1015.28, 1017.46, 1019.13, 1020.62, 1021.46, 1021.8, 1022.63, 1022.69, 1023.22, 1023.29, 1023.52, 1023.72, 1023.67, 1023.81, 1023.85, 1023.88, 1023.86, 1023.95, 1023.88, 1023.96, 1023.97, 1023.97, 1023.97, 1023.99, 1023.99, 1023.99, 1023.98, 1024.0, 1023.97, 1024.0, 1024.0, 1023.99, 1024.0, 1024.0, 1024.0, 1024.0, 1024.0]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1100)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot([-60, 500], [1026, 1026], color='r', linestyle='--')
    plt.plot([300, 300], [0, 1024], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1026, 'y = 1024', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber512", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DRV20_Kyber512_major():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490]
    coe_DRV = [300, 605.65, 745.42, 832.96, 887.6, 925.52, 954.07, 971.37, 985.16, 996.57, 1003.06, 1008.52, 1012.5, 1015.28, 1017.46, 1019.13, 1020.62, 1021.46, 1021.8, 1022.63, 1022.69, 1023.22, 1023.29, 1023.52, 1023.72, 1023.67, 1023.81, 1023.85, 1023.88, 1023.86, 1023.95, 1023.88, 1023.96, 1023.97, 1023.97, 1023.97, 1023.99, 1023.99, 1023.99, 1023.98, 1024.0, 1023.97, 1024.0, 1024.0, 1023.99, 1024.0, 1024.0, 1024.0, 1024.0, 1024.0]
    coe_DRV_s = [150, 287.52, 386.6, 447.48, 478.29, 496.08, 504.7, 508.02, 510.17, 511.16, 511.59, 511.77, 511.95, 511.92, 511.98, 511.99, 511.98, 511.98, 511.99, 511.99, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')
    f2 = interp1d(ine_DRV, coe_DRV_s, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)
    xnew2 = np.linspace(0, 300, 300)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1100)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Our Method')

    plt.plot([-60, 500], [1026, 1026], color='r', linestyle='--')
    plt.plot([-60, 300], [514, 514], color='r', linestyle='--')

    plt.plot([300, 300], [0, 1024], color='blue', linestyle='--')
    plt.plot([120, 120], [0, 512], color='blue', linestyle='--')

    # plt.axvline(x=3000, ymin=0, ymax=512, color='b', linestyle='--', label='x = 3000')

    # 在图中添加标注
    plt.text(-50, 1026, 'y = 1024', color='red', verticalalignment='bottom')
    plt.text(-50, 514, 'y = 512', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber512", fontsize=22)
    plt.xlabel('num of failures', fontsize=22)
    plt.ylabel('recovered coefficients', fontsize=22)

    plt.legend(loc='center', bbox_to_anchor=(0.82, 0.7))
    plt.show()

def coe_ine_DRV20_Kyber768():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430,
               440, 450, 460, 470, 480, 490]

    coe_DRV = [590, 1037.69, 1237.72, 1347.22, 1414.4, 1456.97, 1485.41, 1502.5, 1512.5, 1520.8, 1525.95, 1529.3,
               1531.2, 1532.57, 1533.81, 1534.49, 1535.19, 1535.35, 1535.63, 1535.7, 1535.81, 1535.91, 1535.89, 1535.91,
               1535.95, 1535.96, 1535.96, 1536.0, 1535.99, 1536.0, 1535.98, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0,
               1535.99, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0,
               1536.0]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1630)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot([-60, 500], [1538, 1538], color='r', linestyle='--')
    plt.plot([210, 210], [0, 1538], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1538, 'y = 1536', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber768", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DRV20_Kyber768_major():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490]

    coe_DRV = [590, 1037.69, 1237.72, 1347.22, 1414.4, 1456.97, 1485.41, 1502.5, 1512.5, 1520.8, 1525.95, 1529.3, 1531.2, 1532.57, 1533.81, 1534.49, 1535.19, 1535.35, 1535.63, 1535.7, 1535.81, 1535.91, 1535.89, 1535.91, 1535.95, 1535.96, 1535.96, 1536.0, 1535.99, 1536.0, 1535.98, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1535.99, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0]

    coe_DRV_s = [295, 514.33, 661.76, 725.6, 753.82, 762.04, 765.83, 767.25, 767.69, 767.88, 767.9, 767.95, 768.0, 767.96, 768.0, 767.99, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0, 768.0]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')
    f2 = interp1d(ine_DRV, coe_DRV_s, kind='cubic')
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)
    xnew2 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1630)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Our Method')

    plt.plot([-60, 500], [1538, 1538], color='r', linestyle='--')
    plt.plot([-60, 300], [770, 770], color='r', linestyle='--')

    plt.plot([210, 210], [0, 1536], color='blue', linestyle='--')
    plt.plot([100, 100], [0, 768], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1538, 'y = 1536', color='red', verticalalignment='bottom')
    plt.text(-50, 770, 'y = 768', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber768", fontsize=22)
    plt.xlabel('num of failures', fontsize=22)
    plt.ylabel('recovered coefficients', fontsize=22)

    plt.legend(loc='center', bbox_to_anchor=(0.82, 0.7))
    plt.show()

def coe_ine_DRV20_Kyber1024():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430,
               440, 450, 460, 470, 480, 490]

    coe_DRV = [717, 1126.71, 1364.23, 1519.31, 1634.11, 1722.83, 1788.53, 1838.59, 1880.2, 1911.31, 1938.2, 1958.1, 1975.01, 1989.15, 1999.93, 2008.2, 2016.14, 2021.53, 2027.02, 2029.94, 2034.2, 2035.88, 2037.96, 2039.51, 2040.95, 2042.55, 2043.2, 2044.14, 2044.75, 2045.5, 2045.81, 2046.22, 2046.41, 2046.96, 2046.81, 2047.05, 2047.15, 2047.32, 2047.47, 2047.54, 2047.72, 2047.65, 2047.73, 2047.8, 2047.87, 2047.87, 2047.82, 2047.87, 2047.9, 2047.96]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 2160)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot([-60, 500], [2048, 2048], color='r', linestyle='--')
    plt.plot([480, 480], [0, 2048], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 2050, 'y = 2048', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber1024", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DRV20_Kyber1024_major():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490]
    coe_DRV = [717, 1126.71, 1364.23, 1519.31, 1634.11, 1722.83, 1788.53, 1838.59, 1880.2, 1911.31, 1938.2, 1958.1, 1975.01, 1989.15, 1999.93, 2008.2, 2016.14, 2021.53, 2027.02, 2029.94, 2034.2, 2035.88, 2037.96, 2039.51, 2040.95, 2042.55, 2043.2, 2044.14, 2044.75, 2045.5, 2045.81, 2046.22, 2046.41, 2046.96, 2046.81, 2047.05, 2047.15, 2047.32, 2047.47, 2047.54, 2047.72, 2047.65, 2047.73, 2047.8, 2047.87, 2047.87, 2047.82, 2047.87, 2047.9, 2047.96]
    coe_DRV_s = [364, 534.42, 679.73, 792.02, 872.77, 929.65, 965.12, 987.9, 1002.32, 1010.78, 1015.59, 1018.4, 1021.07, 1022.05, 1022.77, 1023.1, 1023.47, 1023.6, 1023.87, 1023.83, 1023.88, 1023.91, 1023.98, 1023.96, 1023.98, 1024, 1024, 1024, 1023.97, 1024, 1024, 1023.99, 1023.98, 1024, 1024, 1023.99, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')
    f2 = interp1d(ine_DRV, coe_DRV_s, kind='cubic')
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)
    xnew2 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 2160)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Our Method')

    plt.plot([-60, 500], [2050, 2050], color='r', linestyle='--')
    plt.plot([-60, 300], [1026, 1026], color='r', linestyle='--')

    plt.plot([480, 480], [0, 2050], color='blue', linestyle='--')
    plt.plot([210, 210], [0, 1026], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 2050, 'y = 2048', color='red', verticalalignment='bottom')
    plt.text(-50, 1026, 'y = 1024', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber1024", fontsize=22)
    plt.xlabel('num of failures', fontsize=22)
    plt.ylabel('recovered coefficients', fontsize=22)

    plt.legend(loc='center', bbox_to_anchor=(0.82, 0.7))
    plt.show()

def coe_ine_DGJ19_Kyber512():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    coe_DGJ = [300, 300.01, 321.45, 438.85, 582.73, 702.06, 836.8, 930.55, 966.47, 960.95, 912.68, 815.84, 676.64, 537.92, 439.04, 375.62, 336.27, 311.68, 294.58, 286.2, 279.22, 275.08, 270.5, 268.8, 266.94, 263.41, 260.12, 258.71, 257.29, 255.27, 254]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1100)
    plt.xlim(-60, 350)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability method')
    plt.plot([-60, 500], [1026, 1026], color='r', linestyle='--')
    # plt.plot([300, 300], [0, 1024], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1026, 'y = 1024', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber512", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_Kyber512_major():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300]
    coe_DGJ = [300, 300.01, 321.45, 438.85, 582.73, 702.06, 836.8, 930.55, 966.47, 960.95, 912.68, 815.84, 676.64,
               537.92, 439.04, 375.62, 336.27, 311.68, 294.58, 286.2, 279.22, 275.08, 270.5, 268.8, 266.94, 263.41,
               260.12, 258.71, 257.29, 255.27, 254]
    coe_DGJ_s = [150, 151, 155.83, 191.46, 228.68, 254.02, 267.98, 285.77, 306.08, 333.74, 384.16, 437.4, 468.46, 479.17, 488.86, 502.21, 509.71, 511.86, 511.91, 511.67, 511, 508.07, 496.91, 466.45, 416.17, 351.18, 291.68, 240.53, 196.61, 159.99, 130.07]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')
    f2 = interp1d(ine_DGJ, coe_DGJ_s, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)
    xnew2 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1120)
    plt.xlim(-60, 350)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Our method')

    plt.plot([-60, 500], [1026, 1026], color='r', linestyle='--')
    plt.plot([-60, 300], [514, 514], color='r', linestyle='--')

    plt.plot([180, 180], [0, 512], color='blue', linestyle='--')

    # plt.axvline(x=3000, ymin=0, ymax=512, color='b', linestyle='--', label='x = 3000')

    # 在图中添加标注
    plt.text(-50, 1026, 'y = 1024', color='r', verticalalignment='bottom')
    plt.text(-50, 514, 'y = 512', color='r', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber512", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_Kyber768():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300]

    coe_DGJ = [590, 590, 591.71, 659.33, 870.56, 1096.62, 1243.47, 1342.19, 1452.05, 1511.22, 1521.9, 1511.51, 1483.1, 1420.9, 1322.87, 1198.47, 1075.86, 959.61, 872.18, 811.38, 772.98, 748.04, 734.14, 722.63, 717.65, 714.35, 711.21, 706.82, 702.88, 699.83, 696.08]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)
    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1650)
    plt.xlim(-60, 350)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability method')
    plt.plot([-60, 500], [1538, 1538], color='r', linestyle='--')
    # plt.plot([210, 210], [0, 1538], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1538, 'y = 1536', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber768", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_Kyber768_major():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300]

    coe_DGJ = [590, 590, 591.71, 659.33, 870.56, 1096.62, 1243.47, 1342.19, 1452.05, 1511.22, 1521.9, 1511.51, 1483.1,
               1420.9, 1322.87, 1198.47, 1075.86, 959.61, 872.18, 811.38, 772.98, 748.04, 734.14, 722.63, 717.65,
               714.35, 711.21, 706.82, 702.88, 699.83, 696.08]

    coe_DGJ_s = [308, 308, 309.96, 333.44, 363.42, 422.79, 512.44, 574.97, 617.91, 649.8, 689.24, 739.56, 763.17, 767.4, 767.97, 767.98, 767.97, 767.9, 767.65, 766.65, 763.51, 754.37, 738.81, 700.28, 648.43, 601.72, 541.5, 483.78, 442.14, 401.3, 371.91]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')
    f2 = interp1d(ine_DGJ, coe_DGJ_s, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)
    xnew2 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1650)
    plt.xlim(-60, 350)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Our method')

    plt.plot([-60, 500], [1538, 1538], color='r', linestyle='--')
    plt.plot([-60, 300], [770, 770], color='r', linestyle='--')

    plt.plot([140, 140], [0, 768], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1538, 'y = 1536', color='r', verticalalignment='bottom')
    plt.text(-50, 770, 'y = 768', color='r', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber768", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_Kyber1024():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300]

    coe_DGJ = [717, 717, 717.03, 722.13, 770.09, 896.65, 1086, 1280.19, 1444, 1563.63, 1659.68, 1758.77, 1857.29, 1939.56, 1986.01, 2004.22, 2004.57, 1992.01, 1962.97, 1923.68, 1864.57, 1790.18, 1701.08, 1605.63, 1508.06, 1406.13, 1313.18, 1231.05, 1159.43, 1103.58, 1050.37]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 2160)
    plt.xlim(-60, 350)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability method')
    plt.plot([-60, 500], [2048, 2048], color='r', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 2050, 'y = 2048', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber1024", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_Kyber1024_major():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300]

    coe_DGJ = [717, 717, 717.03, 722.13, 770.09, 896.65, 1086, 1280.19, 1444, 1563.63, 1659.68, 1758.77, 1857.29,
               1939.56, 1986.01, 2004.22, 2004.57, 1992.01, 1962.97, 1923.68, 1864.57, 1790.18, 1701.08, 1605.63,
               1508.06, 1406.13, 1313.18, 1231.05, 1159.43, 1103.58, 1050.37]

    coe_DGJ_s = [354, 354, 354, 357.87, 382.14, 418.3, 460.3, 500.78, 556.8, 620.48, 677.58, 729.54, 768.09, 796.44, 838.8, 890.1, 935.52, 981.09, 1006.36, 1017.1, 1021.93, 1023.46, 1023.87, 1023.86, 1023.85, 1023.86, 1023.8, 1023.49, 1022.96, 1021.68, 1019.38]
    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')
    f2 = interp1d(ine_DGJ, coe_DGJ_s, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)
    xnew2 = np.linspace(0, 300, 300)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 2160)
    plt.xlim(-60, 350)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Our method')

    plt.plot([-60, 500], [2050, 2050], color='r', linestyle='--')
    plt.plot([-60, 300], [1026, 1026], color='r', linestyle='--')

    plt.plot([220, 220], [0, 1026], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 2050, 'y = 2048', color='r', verticalalignment='bottom')
    plt.text(-50, 1026, 'y = 1024', color='r', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.title("Kyber1024", fontsize=16)
    plt.xlabel('num of failures', fontsize=16)
    plt.ylabel('recovered coefficients', fontsize=16)

    plt.legend(loc='lower right')
    plt.show()


def coe_ine_DGJ19_DRV20_Kyber512():
    ine_DGJ = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300]
    coe_DGJ = [300, 300.01, 321.45, 438.85, 582.73, 702.06, 836.8, 930.55, 966.47, 960.95, 912.68, 815.84, 676.64,
               537.92, 439.04, 375.62, 336.27, 311.68, 294.58, 286.2, 279.22, 275.08, 270.5, 268.8, 266.94, 263.41,
               260.12, 258.71, 257.29, 255.27, 254]

    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490]
    coe_DRV = [300, 605.65, 745.42, 832.96, 887.6, 925.52, 954.07, 971.37, 985.16, 996.57, 1003.06, 1008.52, 1012.5, 1015.28, 1017.46, 1019.13, 1020.62, 1021.46, 1021.8, 1022.63, 1022.69, 1023.22, 1023.29, 1023.52, 1023.72, 1023.67, 1023.81, 1023.85, 1023.88, 1023.86, 1023.95, 1023.88, 1023.96, 1023.97, 1023.97, 1023.97, 1023.99, 1023.99, 1023.99, 1023.98, 1024.0, 1023.97, 1024.0, 1024.0, 1023.99, 1024.0, 1024.0, 1024.0, 1024.0, 1024.0]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DGJ, coe_DGJ, kind='cubic')
    f2 = interp1d(ine_DRV, coe_DRV, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 300, 300)
    xnew2 = np.linspace(0, 490, 490)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1100)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Probability Method')
    plt.plot(xnew2, f2(xnew2), '-', color='g', label='Geometric Method')
    plt.plot([-60, 500], [1026, 1026], color='r', linestyle='--')
    plt.plot([300, 300], [0, 1024], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1026, 'y = 1024', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.xlabel('num of failures')
    plt.ylabel('recovered coefficients')

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_DRV20_Kyber768():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430,
               440, 450, 460, 470, 480, 490]

    coe_DRV = [590, 1037.69, 1237.72, 1347.22, 1414.4, 1456.97, 1485.41, 1502.5, 1512.5, 1520.8, 1525.95, 1529.3,
               1531.2, 1532.57, 1533.81, 1534.49, 1535.19, 1535.35, 1535.63, 1535.7, 1535.81, 1535.91, 1535.89, 1535.91,
               1535.95, 1535.96, 1535.96, 1536.0, 1535.99, 1536.0, 1535.98, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0,
               1535.99, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0, 1536.0,
               1536.0]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 1630)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot([-60, 500], [1538, 1538], color='r', linestyle='--')
    plt.plot([210, 210], [0, 1538], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 1538, 'y = 1536', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.xlabel('num of failures')
    plt.ylabel('recovered coefficients')

    plt.legend(loc='lower right')
    plt.show()

def coe_ine_DGJ19_DRV20_Kyber1024():
    ine_DRV = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
               230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430,
               440, 450, 460, 470, 480, 490]

    coe_DRV = [717, 1126.71, 1364.23, 1519.31, 1634.11, 1722.83, 1788.53, 1838.59, 1880.2, 1911.31, 1938.2, 1958.1, 1975.01, 1989.15, 1999.93, 2008.2, 2016.14, 2021.53, 2027.02, 2029.94, 2034.2, 2035.88, 2037.96, 2039.51, 2040.95, 2042.55, 2043.2, 2044.14, 2044.75, 2045.5, 2045.81, 2046.22, 2046.41, 2046.96, 2046.81, 2047.05, 2047.15, 2047.32, 2047.47, 2047.54, 2047.72, 2047.65, 2047.73, 2047.8, 2047.87, 2047.87, 2047.82, 2047.87, 2047.9, 2047.96]

    # 使用'cubic'插值创建平滑函数
    f1 = interp1d(ine_DRV, coe_DRV, kind='cubic')

    # 生成细分的x值以绘制平滑曲线
    xnew1 = np.linspace(0, 490, 490)

    # 设置坐标轴纵轴长度为 1000
    plt.ylim(0, 2160)
    plt.xlim(-60, 500)
    # 绘制平滑曲线
    plt.plot(xnew1, f1(xnew1), '-', color='orange', label='Geometric Method')
    plt.plot([-60, 500], [2048, 2048], color='r', linestyle='--')
    plt.plot([480, 480], [0, 2048], color='blue', linestyle='--')

    # 在图中添加标注
    plt.text(-50, 2050, 'y = 2048', color='red', verticalalignment='bottom')

    # 添加坐标轴标签
    plt.xlabel('num of failures')
    plt.ylabel('recovered coefficients')

    plt.legend(loc='lower right')
    plt.show()


def lattice_reduction1():
    x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    y_base = [135, 128, 124, 121, 118, 115, 112, 109, 107, 104, 102, 100, 98, 96]

    y_our = []
    Y = []

    # Read all complexity into Y
    with open("worknextciphertext-LQFalse,MTFalse300-sd1.txt", "r") as f:
        for line in f:
            Y.append(float(line.split(",")[1]))

    # Sum [x, 100] complexities append into y_our
    for _x in x:
        sum = 0
        for idx in range(_x, len(Y)):
            sum += Y[idx]
        y_our.append(math.log2(sum))

    plt.plot(x, y_base, '-', color='orange', label="Lattice reduction")
    plt.plot(x, y_our, '-', color='g', label="Our method")

    plt.ylim(50, 138)

    plt.title("work to recovery the secret key")
    plt.xlabel("the num of collected failures")
    plt.ylabel("the rest complexity")

    plt.legend(loc='lower right')

    plt.show()

def lattice_reduction():
    x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    y_base = [135, 128, 124, 121, 118, 115, 112, 109, 107, 104, 102, 100, 98, 96]
    y_latt = []

    y_our = []
    Y = []

    # Read all complexity into Y
    with open("worknextciphertext-LQFalse,MTFalse300-sd1.txt", "r") as f:
        for line in f:
            Y.append(float(line.split(",")[1]))

    # Sum [x, 100] complexities append into y_our
    for _x in x:
        sum = 0
        for idx in range(_x, len(Y)):
            sum += Y[idx]
        y_our.append(sum)

    for i in range(len(x)):
        y_latt.append(2 ** y_base[i])

    fig, ax = plt.subplots()

    ax.plot(x, y_latt, '-', color='orange', label="Lattice reduction")
    ax.plot(x, y_our, '-', color='g', label="Our method")
    # ax.set_xscale('log', base=2)
    ax.set_yscale('log', base=2)
    ax.set_ylim(bottom=2 ** 30)

    plt.title("work to recovery the secret key for Kyber768", fontsize=16)
    plt.xlabel("num of collected failures",fontsize=16)
    plt.ylabel("complexity",fontsize=16)

    plt.legend(loc='lower right')

    plt.show()

def next_work():
    x = np.arange(0, 100, 1)
    y = []

    # Read all complexity into Y
    with open("worknextciphertext-LQFalse,MTFalse300-sd1.txt", "r") as f:
        for line in f:
            y.append(float(line.split(",")[1]))

    fig, ax = plt.subplots()

    ax.plot(x,y,label='Directional failure boosting')
    # ax.set_xscale('log', base=2)
    ax.set_yscale('log', base=2)
    ax.set_ylim(bottom=2**20)
    plt.title("work to obtain next failure for Kyber768", fontsize=16)
    plt.xlabel("the num of collected failures", fontsize=16)
    plt.ylabel("the complexity", fontsize=16)

    plt.legend(loc='lower right')

    plt.show()

if __name__ == '__main__':
    # the relation of num of ineqs and recovered coes
    # coe_ine_DGJ19_Kyber512()
    # coe_ine_DGJ19_Kyber768()
    # coe_ine_DGJ19_Kyber1024()
    # coe_ine_DGJ19_Kyber512_major()
    # coe_ine_DGJ19_Kyber768_major()
    # coe_ine_DGJ19_Kyber1024_major()
    #
    # coe_ine_DRV20_Kyber512()
    # coe_ine_DRV20_Kyber768()
    # coe_ine_DRV20_Kyber1024()
    coe_ine_DRV20_Kyber512_major()
    coe_ine_DRV20_Kyber768_major()
    coe_ine_DRV20_Kyber1024_major()

    # coe_ine_DGJ19_DRV20_Kyber512()

    # lattice_reduction()
    # next_work()



