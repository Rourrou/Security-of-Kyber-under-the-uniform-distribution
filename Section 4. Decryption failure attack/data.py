import numpy as np
import matplotlib.pyplot as plt
from Major_vote.df_6000.inequalities import coeffs, signs, bs, is_corrects, p_corrects


# 定义 rotation 函数
def split_ineq():
    block = 3000
    coe_1 = coeffs[:4000]
    sig_1 = signs[:4000]
    bs_1 = bs[:4000]
    is_1 = is_corrects[:4000]
    p_1 = p_corrects[:4000]
    with open('inequalities_1.py', 'w') as file:
        coe1_str = repr(coe_1.tolist()) if isinstance(coe_1, np.ndarray) else repr(coe_1)
        file.write(f"coeffs = {coe1_str}\n")
        sig1_str = repr(sig_1.tolist()) if isinstance(sig_1, np.ndarray) else repr(sig_1)
        file.write(f"signs = {sig1_str}\n")
        bs1_str = repr(bs_1.tolist()) if isinstance(bs_1, np.ndarray) else repr(bs_1)
        file.write(f"bs = {bs1_str}\n")
        is1_str = repr(is_1.tolist()) if isinstance(is_1, np.ndarray) else repr(is_1)
        file.write(f"is_corrects = {is1_str}\n")
        p1_str = repr(p_1.tolist()) if isinstance(p_1, np.ndarray) else repr(p_1)
        file.write(f"p_corrects = {p1_str}\n")

    coe_2 = coeffs[1000: 5000]
    sig_2 = signs[1000: 5000]
    bs_2 = bs[1000: 5000]
    is_2 = is_corrects[1000: 5000]
    p_2 = p_corrects[1000: 5000]
    with open('inequalities_2.py', 'w') as file:
        coe2_str = repr(coe_2.tolist()) if isinstance(coe_2, np.ndarray) else repr(coe_2)
        file.write(f"coeffs = {coe2_str}\n")
        sig2_str = repr(sig_2.tolist()) if isinstance(sig_2, np.ndarray) else repr(sig_2)
        file.write(f"signs = {sig2_str}\n")
        bs2_str = repr(bs_2.tolist()) if isinstance(bs_2, np.ndarray) else repr(bs_2)
        file.write(f"bs = {bs2_str}\n")
        is2_str = repr(is_2.tolist()) if isinstance(is_2, np.ndarray) else repr(is_2)
        file.write(f"is_corrects = {is2_str}\n")
        p2_str = repr(p_2.tolist()) if isinstance(p_2, np.ndarray) else repr(p_2)
        file.write(f"p_corrects = {p2_str}\n")

    coe_3 = coeffs[2000:]
    sig_3 = signs[2000:]
    bs_3 = bs[2000:]
    is_3 = is_corrects[2000:]
    p_3 = p_corrects[2000:]
    with open('inequalities_3.py', 'w') as file:
        coe3_str = repr(coe_3.tolist()) if isinstance(coe_3, np.ndarray) else repr(coe_3)
        file.write(f"coeffs = {coe3_str}\n")
        sig3_str = repr(sig_3.tolist()) if isinstance(sig_3, np.ndarray) else repr(sig_3)
        file.write(f"signs = {sig3_str}\n")
        bs3_str = repr(bs_3.tolist()) if isinstance(bs_3, np.ndarray) else repr(bs_3)
        file.write(f"bs = {bs3_str}\n")
        is3_str = repr(is_3.tolist()) if isinstance(is_3, np.ndarray) else repr(is_3)
        file.write(f"is_corrects = {is3_str}\n")
        p3_str = repr(p_3.tolist()) if isinstance(p_3, np.ndarray) else repr(p_3)
        file.write(f"p_corrects = {p3_str}\n")

    return 1


if __name__ == '__main__':
    print(coeffs[0])
    k = 3  # 分组个数
    split_ineq()