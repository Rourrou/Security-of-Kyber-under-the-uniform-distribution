import numpy as np
import random
import os
import glob

# recover the relative position of dfi with dfs by iterative
def filter():
    A = np.loadtxt("Kyber512_uniform/33322/all/A.txt", dtype=np.int16)
    b = np.loadtxt("Kyber512_uniform/33322/all/b.txt", dtype=np.int16)
    epp = np.loadtxt("Kyber512_uniform/33322/all/epp.txt", dtype=np.int16)
    sign = np.loadtxt("Kyber512_uniform/33322/all/sign.txt", dtype=np.int16)

    m, n = A.shape
    print("m, n", m, n)

    # 将每一行转换为一个可哈希的类型（例如元组），并存储唯一的行
    unique_lines = set()
    unique_vectors = []

    for i in range(m):
        vector = tuple(map(int, A[i]))
        # 检查向量或其相反向量是否已存在
        if vector not in unique_lines:
            unique_lines.add(vector)
            unique_vectors.append(vector)

            # 将唯一的向量写入新文件
            with open('Kyber512_uniform/33322/all/Filter/A.txt', 'a') as file_A:
                line = ' '.join(map(str, vector)) + '\n'
                file_A.write(line)
            with open('Kyber512_uniform/33322/all/Filter/b.txt', 'a') as file_b:
                file_b.write(f"{b[i]}\n")
            with open('Kyber512_uniform/33322/all/Filter/epp.txt', 'a') as file_epp:
                file_epp.write(f"{epp[i]}\n")
            with open('Kyber512_uniform/33322/all/Filter/sign.txt', 'a') as file_sign:
                file_sign.write(f"{sign[i]}\n")

    print("the number of filtered df is ", len(unique_vectors))


def df_test():
    A = np.loadtxt("Kyber512_uniform/33322/all/Filter/A.txt", dtype=np.int16)
    b = np.loadtxt("Kyber512_uniform/33322/all/Filter/b.txt", dtype=np.int16)
    es = np.loadtxt("Kyber512_uniform/33322/e_s.txt", dtype=np.int16)
    epp = np.loadtxt("Kyber512_uniform/33322/all/Filter/epp.txt", dtype=np.int16)
    sign = np.loadtxt("Kyber512_uniform/33322/all/Filter/sign.txt", dtype=np.int16)

    m, n = A.shape
    print("m, n", m, n)

    for i in range(m):
        noisy = np.dot(A[i], es)
        noisy = noisy+epp[i]
        print(noisy)


# integrate all ineqs into one txt
def integrate():
    # 定义文件夹和目标文件的路径
    folder_path = 'Kyber512_uniform/33322/ryc/20240121/data'
    output_file = 'Kyber512_uniform/33322/ryc/20210121.txt'

    # 检索文件夹中所有的.txt文件
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    # 将所有.txt文件的内容拼接到一个文件中
    with open(output_file, 'w') as outfile:
        for txt in txt_files:
            with open(txt, 'r') as infile:
                outfile.write(infile.read())  # 在文件内容之间添加换行符

    # 输出结果文件的路径
    output_file


if __name__ == '__main__':
    # integrate all ineqs
    # integrate()

    # Remove duplicate data
    # filter()

    # testing the decryption failure
    df_test()



