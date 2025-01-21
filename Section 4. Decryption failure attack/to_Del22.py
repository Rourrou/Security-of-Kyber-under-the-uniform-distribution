import numpy as np
import matplotlib.pyplot as plt

def A_double(m):
    # 读取A.txt文件内容
    with open("A.txt", "r") as txt_file:
        lines = txt_file.readlines()[:m]
    # 创建A_double.txt并写入内容
    with open("A_double.txt", "w") as py_file:
        for line in lines:
            py_file.write(f"{line}")
            py_file.write(f"{line}")


def b_double(m):
    # 读取b.txt文件内容
    with open("b.txt", "r") as txt_file:
        lines = txt_file.readlines()[:m]
    # 创建A_double.txt并写入内容
    with open("b_double.txt", "w") as py_file:
        for line in lines:
            py_file.write(f"{line}")

            if int(line) > 0:
                py_file.write(f"{832}\n")
            else:
                py_file.write(f"{-832}\n")



if __name__ == '__main__':
    m = 8000
    A_double(m)
    b_double(m)