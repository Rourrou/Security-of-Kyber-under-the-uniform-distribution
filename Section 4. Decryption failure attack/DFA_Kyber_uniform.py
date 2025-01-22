#!/usr/bin/python3
import random
import numpy as np
from scipy.stats import mode, norm, uniform
from tqdm import tqdm


def evaluate_inequalities_fast(a, b, solution):  # evaluate the direction of inequalities
    return (np.matmul(a, solution) - b) >= 0


def major_vote_any_512(a, solution):
    a = np.array(a)
    [nb_of_inequalities, nb_of_unknowns] = a.shape
    # 初始化众数数组和众数出现次数
    guess_mode = np.zeros(nb_of_unknowns, dtype=int)
    counts = np.zeros(nb_of_unknowns, dtype=int)

    # 计算众数和众数出现次数
    for i in range(nb_of_unknowns):
        mode_info = mode(a[:, i])
        guess_mode[i] = mode_info.mode
        counts[i] = mode_info.count
    # print("众数数组：", guess_mode)
    # print("众数出现次数：", counts)

    nb_correct = np.count_nonzero(solution == guess_mode)
    # print("Number of correctly guessed unknowns: {:d}/{:d}".format(nb_correct, nb_of_unknowns))
    # print("guess:", np.array(guess_mode))


    # 对数组进行降序排序
    sorted_counts = np.argsort(counts)[::-1]
    # 选择前512个最大元素的索引
    half = int(nb_of_unknowns/2)
    index_pro = sorted_counts[:half]
    # 使用index_pro
    selected_guess = guess_mode[index_pro]
    selected_solution = solution[index_pro]
    matches = selected_guess == selected_solution
    num_of_matches = np.count_nonzero(matches)
    # print("Number of selected coeffs matches:{:d}/{:d}".format(num_of_matches, half))

    return num_of_matches


def solve_inequalities(eta, a, b, is_geq_zero, solution):
    # print("Solving inequalities...")

    [nb_of_inequalities, nb_of_unknowns] = a.shape

    # as>b
    for i in range(0, nb_of_inequalities):
        if is_geq_zero[i]:
            a[i] = np.array(a[i])
            b[i] = b[i]
        else:
            a[i] = np.array(-a[i])
            b[i] = -b[i]

    guess = np.zeros(nb_of_unknowns, dtype=int)  # creat an initial guess of the solution with all values set to zero

    if nb_of_inequalities == 0:
        return guess
    nb_of_values = 2*eta + 1
    x = np.arange(-eta, eta + 1, dtype=np.int8)
    # x_pmf = binom.pmf(x + eta, 2 * eta, 0.5)
    x_pmf = uniform.cdf(x+1, -eta, 2*eta+1) - uniform.cdf(x, -eta, 2*eta+1)
    # print("x_pmf", x_pmf)
    x_pmf = np.repeat(x_pmf.reshape(1,-1), nb_of_unknowns, axis=0) # this line repeats the x_pmf array multiple times to creat a 2D array
    a = a.astype(np.int16) # this change the datatype of the matrix a to int16
    a_squared = np.square(a) # this squares each element of a

    mean = np.matmul(x_pmf, x)  # 计算当前分布下，所有未知数的期望值
    variance = np.matmul(x_pmf, np.square(x)) - np.square(mean)  # 方差计算公式
    mean = np.multiply(a, np.repeat(mean[np.newaxis, :],
                                    nb_of_inequalities, axis=0))
    variance = np.multiply(
        a_squared,
        np.repeat(variance[np.newaxis, :], nb_of_inequalities, axis=0))
    # mean_all = mean.sum(axis=1).reshape(-1, 1).repeat(nb_of_unknowns, axis=1)
    mean = mean.sum(axis=1).reshape(-1, 1).repeat(nb_of_unknowns, axis=1) - mean
    # print("mean", mean)
    # mean -= b[:, np.newaxis]
    # mean_all += b[:, np.newaxis]
    mean += 800 # 实验表明，750， 800效果最佳
    # variance_all = variance.sum(axis=1).reshape(-1, 1).repeat(nb_of_unknowns, axis=1)
    variance = variance.sum(axis=1).reshape(-1, 1).repeat(nb_of_unknowns, axis=1) - variance
    # print("variance", variance)
    variance = np.clip(variance, 1, None)
    psuccess = np.zeros((nb_of_values, nb_of_inequalities,
                         nb_of_unknowns), dtype=float)
    for j in range(nb_of_values):
        zscore = np.divide(a * x[j] + mean + 0.5, np.sqrt(variance))
        # zscore = np.divide(a * x[j] + mean + 6*np.sqrt(variance), np.sqrt(variance))
        # print("norm.cdf(zscore)", norm.cdf(np.divide(100, np.sqrt(14500))))
        # psuccess[j, :, :] = norm.cdf(zscore) / norm.cdf(np.divide(mean + 0.5, np.sqrt(variance))) # central limit theorem
        psuccess[j, :, :] = norm.cdf(zscore) # / norm.cdf(np.divide(mean_all, np.sqrt(variance_all)))
        # print("psuccess[j, 0, 0]", psuccess[j, 0, 0])
    psuccess = np.transpose(psuccess, axes=[2, 0, 1])
    psuccess = np.sum(np.log(psuccess), axis=2)
    # print("psuccess", psuccess)
    psuccess = np.exp(psuccess)
    # psuccess = np.sum(psuccess)

    x_pmf = np.multiply(psuccess, x_pmf)
    # print("x_pmf", x_pmf)
    row_sums = x_pmf.sum(axis=1)
    x_pmf /= row_sums[:, np.newaxis]

    # for i in range(3):
    #     print("x_pmf%d" %i)
    #     for element in x_pmf[i]:
    #         print(f"{element:.16f}")
    guess_ave = np.matmul(x_pmf, x)
    # print("guess_ave", guess_ave)


    max_pro = np.max(x_pmf, axis=1)
    # print("max_pro", max_pro)
    # print("max_pro_0,max_pro_1,max_pro_2,max_pro_3)", max_pro[0],max_pro[1], max_pro[2],max_pro[3])
    # 对数组进行降序排序
    sorted_indices = np.argsort(max_pro)[::-1]
    # print("sorted_indices", sorted_indices)
    # 选择前512个最大元素的索引
    index_pro = sorted_indices[:512]
    guess = x[np.argmax(x_pmf, axis=1)]
    # print("guess ", guess)

    if solution is not None:
        nb_correct = np.count_nonzero(solution == guess)
        # print("Number of correctly guessed unknowns: {:d}/{:d}".format(nb_correct, len(solution)))

    # 使用index_pro
    selected_guess = guess[index_pro]
    selected_solution = solution[index_pro]
    matches = selected_guess == selected_solution
    num_of_matches = np.count_nonzero(matches)
    # print("Number of selected coeffs matches:{:d}/512".format(num_of_matches))

    return guess, nb_correct


def block_BP_major_vote_512(n, m, k, solution):
    eta = 3
    nb_of_inequalities = n
    print("The number of equalities is", nb_of_inequalities)

    with open("DATA/uKyber512/A.txt", 'r') as f:
        lines_a = [next(f) for _ in range(nb_of_inequalities)]
        a = np.loadtxt(lines_a)
        a = a[:n]

    with open("DATA/uKyber512/b.txt", 'r') as g:
        lines_b = [next(g) for _ in range(nb_of_inequalities)]
        b = np.loadtxt(lines_b)
        b = b[:n]

    if m > n:
        raise ValueError("the select ine is more than the data")

    nb_correct = [0] * k
    tag = 0
    guess_block = []
    for i in range(k):
        # 选择m个索引
        indices = random.sample(range(n), m)
        a_selected = np.array([a[j] for j in indices])
        b_selected = np.array([b[j] for j in indices])
        is_geq_zero = evaluate_inequalities_fast(a_selected, b_selected, solution)
        guess, nb_correct[i] = solve_inequalities(eta, a_selected, b_selected, is_geq_zero, solution=solution)
        guess_block.append(guess)

    num_of_matches = major_vote_any_512(guess_block, solution)
    print("the average recovered coefficients with %d ineqs is %d" % (m, num_of_matches))
    return num_of_matches


def dfa_prob(m, solution):
    """Solves one system of inequalities and tracks the convergence rate"""
    eta = 3
    nb_of_inequalities = 27483
    # print("The number of equalities is", m)

    with open("DATA/uKyber512/A.txt", 'r') as f:
        lines_a = [next(f) for _ in range(nb_of_inequalities)]
    a = np.loadtxt(lines_a)
    with open("DATA/uKyber512/b.txt", 'r') as g:
        lines_b = [next(g) for _ in range(nb_of_inequalities)]
    b = np.loadtxt(lines_b)

    [nb_of_inequalities, nb_of_unknowns] = a.shape
    if m == 0:
        E_int = [0] * nb_of_unknowns
        nb_correct = np.count_nonzero(solution == E_int)
        print("the average recovered coefficients with %d ineqs is %d" % (m, nb_correct))
        return nb_correct

    # 选择m个索引
    indices = random.sample(range(nb_of_inequalities), m)
    a_selected = np.array([a[j] for j in indices])
    b_selected = np.array([b[j] for j in indices])
    is_geq_zero = evaluate_inequalities_fast(a_selected, b_selected, solution)

    s, n = solve_inequalities(eta, a_selected, b_selected, is_geq_zero, solution=solution)
    print("the recovered coefficients with %d ineqs is %f" % (m, n))

    return n


if __name__ == "__main__":
    solution = []
    with open("DATA/uKyber512/e_s.txt", 'r') as g:
        for line in g:
            solution.append(int(line.strip()))
    solution = np.array(solution)

    # probability method
    for m in tqdm(range(100, 15000, 100)):
        num_of_matches = []
        num_correct = 0
        for test in range(10):
            num = dfa_prob(m, solution)
            num_of_matches.append(num)
            if num == 1024:
                num_correct += 1
        ave = np.sum(num_of_matches)
        print("the number of matched coefficient with %d ineqs using major vote method with block size %d, is %f/1024"
              %(m, m/2, ave/10))
        print("the success prob of recovering full ineqs with %d ineqs is %f" % (m, num_correct / 10))


    # major vote
    for m in tqdm(range(100, 5000, 100)):
        num_of_matches = []
        num_correct = 0
        for test in range(10):
            num = block_BP_major_vote_512(m, int(m/2), 23, solution)
            num_of_matches.append(num)
            if num == 512:
                num_correct += 1
        ave = np.sum(num_of_matches)
        print("the number of matched coefficient with %d ineqs using major vote method with block size %d, is %f/512"
              %(m, m/2, ave/10))
        print("the success prob of recovering full ineqs with %d ineqs is %f" % (m, num_correct / 10))


