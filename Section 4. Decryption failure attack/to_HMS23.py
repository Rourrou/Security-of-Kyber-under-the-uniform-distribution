import numpy as np
import matplotlib.pyplot as plt

def inequalities(m):
    # 读取txt文件内容
    with open("A.txt", "r") as txt_file:
        lines = txt_file.readlines()[:m]

    # 创建.py文件并写入内容
    with open("inequalities.py", "w") as py_file:
        py_file.write(f"coeffs = [\n")

        for line in lines:
            # 移除行尾的换行符，并按空格分割元素
            elements = line.strip().split(" ")
            # 将元素组合成字符串，用逗号加空格隔开
            vector_str = ", ".join(elements)
            # 写入到.py文件中
            py_file.write(f"[{vector_str}],\n")
        py_file.write(f"]\n")


def signs(m):
    with open("sign.txt", "r") as txt_file:
        lines = txt_file.readlines()[:m]
    # 创建.py文件并写入内容
    print(lines[0])
    with open("inequalities.py", "a") as py_file:
        py_file.write(f"signs = [\n")
        for i in range(m):
            if int(lines[i]) == 0:
                py_file.write(f'"<=",\n')
            elif int(lines[i]) == 1:
                py_file.write(f'">=",\n')
        py_file.write(f"]\n")


# abs(bs)-512, 使得概率不被置0
def bs(m):
    with open("b.txt", "r") as txt_file:
        lines = txt_file.readlines()[:m]

    with open("inequalities.py", "a") as py_file:
        py_file.write(f"bs = [\n")
        for i in range(m):
            b = int(lines[i])
            py_file.write(f"{b},\n")
            # if b > 512:
            #     py_file.write(f"{b-512},\n")
            # else:
            #     py_file.write(f"{b+512},\n")
        py_file.write(f"]\n")


def is_corrects(m):
    with open("inequalities.py", "a") as py_file:
        py_file.write(f"is_corrects = [\n")
        for i in range(m):
            py_file.write(f"True,\n")
        py_file.write(f"]\n")

def p_corrects(m):
    with open("inequalities.py", "a") as py_file:
        py_file.write(f"p_corrects = [\n")
        for i in range(m):
            py_file.write(f"1,\n")
        py_file.write(f"]\n")


def run_data(m):
    # 读取txt文件内容
    with open("e_s.txt", "r") as txt_file:
        lines = txt_file.readlines()

    # 创建.py文件并写入内容
    with open("run_data.py", "w") as py_file:
        py_file.write(f"key_e = [")
        for line in lines[:512]:
            # 移除行尾的换行符，并按空格分割元素
            elements = line.strip().split(" ")[0]

            py_file.write(f"{elements}, ")
        py_file.write(f"]\n")

        py_file.write(f"key_s = [")
        for line in lines[512:]:
            # 移除行尾的换行符，并按空格分割元素
            elements = line.strip().split(" ")[0]

            py_file.write(f"{elements}, ")
        py_file.write(f"]\n")

        py_file.write(f"key = key_e + key_s\n")
        py_file.write(f"max_delta_v = None\n")
        py_file.write(f"filtered_cts = {m}\n")
        py_file.write(f"ineqs = {m}\n")
        py_file.write(f"correct_ineqs = {m}\n")
        py_file.write(f"recovered_coefficients = {m}\n")


def lwe_instance():

    with open("lwe_instance.py", "w") as py_file:
        py_file.write(f"a = []\n")
        py_file.write(f"b = []\n")

    with open("e_s.txt", "r") as txt_file:
        lines = txt_file.readlines()
    # 创建.py文件并写入内容
    with open("lwe_instance.py", "a") as py_file:
        py_file.write(f"e = [")
        for line in lines[:512]:
            # 移除行尾的换行符，并按空格分割元素
            elements = line.strip().split(" ")[0]

            py_file.write(f"{elements}, ")
        py_file.write(f"]\n")

        py_file.write(f"s = [")
        for line in lines[512:]:
            elements = line.strip().split(" ")[0]

            py_file.write(f"{elements}, ")
        py_file.write(f"]\n")

        py_file.write(f"key = e + s\n")


if __name__ == '__main__':
    m = 20
    inequalities(m)
    signs(m)
    bs(m)
    is_corrects(m)
    p_corrects(m)

    run_data(m)
    lwe_instance()
