import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # 绘制密度曲线
import random
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14


# 定义 rotation 函数
def rotation(b, i):
    n = len(b)
    rotated_b = np.concatenate([-b[n-i:], b[:n-i]])
    return rotated_b


def mod_rotation(b, i, m):
    n = len(b)
    output = np.zeros(n)
    for k in range(int(n/m)):
        tmp = b[m*k: m*(k+1)]
        tmp = rotation(tmp, i)
        output[m*k: m*(k+1)] = tmp
    return output


def dot_products(matrix, vec):
    """Calculate dot products of a vector with every rotation of all vectors in a matrix."""
    n = len(vec)
    m = matrix.shape[0]
    results = []

    for j in range(m):  # For each vector in matrix
        for k in range(n):  # For each rotation of matrix[j]
            results.append(np.dot(vec, rotation(matrix[j], k)))

    # Plotting
    plt.hist(results, bins=50, edgecolor='k')
    plt.title("Distribution of Dot Products {i}")
    plt.xlabel("Dot Product Value")
    plt.ylabel("Frequency")
    plt.show()

    return results


# calculate the sign of epp matches the direction of df
def sign_match():
    A_full = np.loadtxt("Kyber512_uniform/failures/A.txt", dtype=np.int16)
    sign_full = np.loadtxt("Kyber512_uniform/failures/sign.txt", dtype=np.int16)
    epp = np.loadtxt("Kyber512_uniform/failures/epp.txt", dtype=np.int16)
    m, n = A_full.shape
    print("m=", m, ", n=", n)

    count = 0
    for i in range(m):
        if sign_full[i] == 1 and epp[i] >= 0:
            count += 1
        elif sign_full[i] == 0 and epp[i] < 0:
            count += 1
        if sign_full[i] == 0:
            A_full[i] = -A_full[i]
    print("the sign of epp matches the direction of df", count / m)


# describe the distribution of |G[i]| of df
def epp_dis():
    A_full = np.loadtxt("Kyber512_uniform/failures/A.txt", dtype=np.int16)
    epp = np.loadtxt("Kyber512_uniform/failures/epp.txt", dtype=np.int16)
    m, n = A_full.shape
    print("m=", m, "n=", n)

    count_epp = 0
    for j in range(len(epp)):
        epp[j] = abs(epp[j])
        if epp[j] > 53:
            count_epp += 1
    print("the probability of |epp| > 53 when decryption failure ", count_epp / m)

    # 绘制分布直方图
    plt.hist(epp, bins='auto', alpha=0.7, rwidth=0.85)
    plt.title('distribution histogram of |G[r]|', fontsize=16)
    plt.xlabel('value', fontsize=16)
    plt.ylabel('frequency', fontsize=16)
    # 添加x=12000的蓝色竖线
    plt.axvline(x=80, color='r', linestyle='--')
    plt.grid(axis='y', alpha=0.75)
    plt.show()


# describe the correlation of ff & fs
def cor_df():
    A = np.loadtxt("Kyber512_uniform/failures/A.txt", dtype=np.int16)
    A_pos = A.copy()
    sign = np.loadtxt("Kyber512_uniform/failures/sign.txt", dtype=np.int16)
    secret = np.loadtxt("Kyber512_uniform/failures/e_s.txt", dtype=np.int16)
    print(A)
    m, n = A.shape
    print("m=", m, "n=", n)
    for i in range(m):
        if sign[i] == 0:
            A_pos[i] = -A_pos[i]

    test_num = 10000
    # test_num = 100
    ff = []
    fs = []
    kf = []
    ks = []
    num = 0  # the number of abs(ff) > abs (fs)
    for i in range(test_num):
        rn = random.sample(range(m), 3)
        b_1 = A_pos[rn[0]]
        b_2 = A_pos[rn[1]]
        b_3 = A_pos[rn[2]]
        inn1 = np.dot(b_1, b_2)
        ff.append(inn1)
        # 私钥和解密失败的内积
        inn11 = np.dot(b_1, secret)
        kf.append(inn11)

        r = random.randint(1, 256)
        b_3 = mod_rotation(b_3, r, 256)
        inn2 = np.dot(b_1, b_3)
        fs.append(inn2)
        # 私钥和解密成功的内积
        inn22 = np.dot(b_3, secret)
        ks.append(inn22)

        if abs(inn1) > abs(inn2):
            num += 1
    print("the probability of fail-fail > fail-scuess", num / test_num)

    # 创建直方图并叠加概率密度曲线
    # fig, ax = plt.subplots()
    # sns.kdeplot(ff, ax=ax, label='failure-failure', fill=True)
    # sns.kdeplot(fs, ax=ax, label='failure-success', fill=True)
    # ax.legend()
    # ax.set_xlabel('correlation',fontsize=16)
    # ax.set_ylabel('probability',fontsize=16)
    # plt.show()

    # 创建直方图并叠加概率密度曲线
    fig, ax = plt.subplots()
    # sns.kdeplot(kf, ax=ax, label='secret-failure', fill=True)
    # sns.kdeplot(ks, ax=ax, label='secret-success', fill=True)
    # 中文投稿
    sns.kdeplot(kf, ax=ax, label='私钥-失败向量', fill=True)
    sns.kdeplot(ks, ax=ax, label='私钥-成功向量', fill=True)
    ax.legend(prop={'size': 14})
    # plt.title('correlation between secret key with success/failure', fontsize=16)
    # ax.set_xlabel('correlation', fontdict={'family': 'Times New Roman', 'size': 14})
    # ax.set_ylabel('probability', fontdict={'family': 'Times New Roman', 'size': 14})
    ax.set_xlabel('相关性', fontdict={'family': 'Times New Roman', 'size': 14})
    ax.set_ylabel('概率', fontdict={'family': 'Times New Roman', 'size': 14})
    plt.show()


# Identifying the position of decryption failure using method in D'Anvers et al
def pos_df0():
    A = np.loadtxt("Kyber512_uniform/failures/A.txt", dtype=np.int16)
    m, n = A.shape
    print("m=", m, "n=", n)

    test_num = 10000
    suc_num = 0
    for i in range(test_num):
        print(f"\rProgress: {i+1}/{test_num}", end='')

        rn = random.sample(range(m), 2)
        df0 = A[rn[0]].copy()
        df0 = df0 / np.linalg.norm(df0)
        df1 = A[rn[1]].copy()
        df1 = df1 / np.linalg.norm(df1)
        # print(df1)

        max_inn = 0
        max_pos_r = 0
        for r in range(256):
            inn = abs(np.dot(df0, mod_rotation(df1, r, 256)))
            if inn > max_inn:
                max_inn = inn
                max_pos_r = r
        if max_pos_r == 0:
            suc_num += 1
        # print(max_inn, i, max_pos_r)
    print("\nexperimental probability of identifying the position of decryption failure using method in D'Anvers et al, "
          "successpro %f" %(float(suc_num / test_num)))


# recover the relative position of dfi with dfs by iterative
def pos_dfs_ite(known_num):
    A = np.loadtxt("Kyber512_uniform/3000/A.txt", dtype=np.int16)
    A_pos = A.copy()
    sign = np.loadtxt("Kyber512_uniform/3000/b.txt", dtype=np.int16)
    m, n = A.shape
    #m = 10
    print("m=", m, "n=", n)
    for i in range(m):
        if sign[i] == 0:
            A_pos[i] = -A_pos[i]
    print(A_pos)

    sum_num = known_num
    ite_num = 3
    # calculate the success probability
    suc_pro = 0
    print("Given %d decryption failure vectors" % sum_num)
    for test in range(100):
        # 从0到cip_num之间随机选择sum_num个不同的数
        rn = random.sample(range(m), sum_num)
        # 将这sum_num个不同的向量加起来，当作密钥估计的初始值
        b_1 = A_pos[rn[0]].copy()
        b_1 = b_1 / np.linalg.norm(b_1)
        for i in range(1, sum_num):
            # b_1 += A_pos[rn[i]]
            b_1 += A_pos[rn[i]] / np.linalg.norm(A_pos[rn[i]])
        #
        b_1 = b_1 / np.linalg.norm(b_1)
        print(b_1)

        del_pos = []
        del_rot = []
        for i in range(sum_num):
            del_pos.append(rn[i])
            del_rot.append(0)

        suc_num1 = 0
        for df in range(m-sum_num):
            # print("del_pos = ", del_pos)
            # print("del_rot = ", del_rot)
            max_inn = 0
            max_pos_i = 0
            max_pos_r = 0
            for i in range(m):  # For each rotation of vec
                if i not in del_pos:
                    for r in range(256):
                        inn = abs(np.dot(b_1, mod_rotation(A_pos[i], r, 256)))
                        if inn > max_inn:
                            max_inn = inn
                            max_pos_i = i
                            max_pos_r = r
            # b_1 += mod_rotation(A_pos[max_pos_i], max_pos_r, 256)
            b_1 += mod_rotation(A_pos[max_pos_i], max_pos_r, 256) / np.linalg.norm(A_pos[max_pos_i])
            del_pos.append(max_pos_i)
            del_rot.append(max_pos_r)
            if max_pos_r == 0:
                suc_num1 += 1
            print(max_inn, max_pos_i, max_pos_r)
        print("the", test + 1, "test's success number1 is", suc_num1)

        for ite in range(1, ite_num):
            suc_num2 = 0
            for df in range(m):
                max_inn = 0
                max_pos_r = 0
                for r in range(256):
                    inn = abs(np.dot(b_1, mod_rotation(A_pos[del_pos[df]], r, 256)))
                    if inn > max_inn:
                        max_inn = inn
                        max_pos_r = r
                if max_pos_r == 0:
                    suc_num2 += 1
                if max_pos_r != del_rot[df]:
                    b_1 -= mod_rotation(A_pos[del_pos[df]], del_rot[df], 256) / np.linalg.norm(A_pos[del_pos[df]])
                    b_1 += mod_rotation(A_pos[del_pos[df]], max_pos_r, 256) / np.linalg.norm(A_pos[del_pos[df]])
                    del_rot[df] = max_pos_r
                print(max_inn, del_pos[df], max_pos_r)

            print("the %d test's success number%d is %d" % (test + 1, ite+1, suc_num2))
            if suc_num2 == m:
                break

        if suc_num2 == m:
            suc_pro += 1
    print("the success probability with", sum_num, "number df is", suc_pro / 100)


if __name__ == '__main__':
    # calculate the sign of epp matches the direction of df
    # sign_match()

    # describe the distribution of |G[i]| of df
    # epp_dis()

    # describe the correlation of ff & fs
    cor_df()

    # recover the relative position of dfi with df0
    #pos_df0()

    # recover the relative position of dfi with dfs by iterative
    # for i in range(1, 5, 1):
    #     pos_dfs_ite(i)



