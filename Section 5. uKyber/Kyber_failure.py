import operator as op
from math import factorial as fac
from math import sqrt, log
import sys
from proba_util import *
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet, MLWE_optimize_attack

class KyberParameterSet:
    def __init__(self, n, m, ks, ke,  q, rqk, rqc, rq2, ke_ct=None):
        if ke_ct is None:
            ke_ct = ke
        self.n = n
        self.m = m
        self.ks = ks     # binary distribution for the secret key
        self.ke = ke    # binary distribution for the ciphertext errors
        self.ke_ct = ke_ct    # binary distribution for the ciphertext errors
        self.q = q
        self.rqk = rqk  # 2^(bits in the public key)
        self.rqc = rqc  # 2^(bits in the first ciphertext)
        self.rq2 = rq2  # 2^(bits in the second ciphertext)

def p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_centered_binomial_law(ps.ks)           # LWE error law for the key
    chie = build_centered_binomial_law(ps.ke_ct)        # LWE error law for the ciphertext
    chie_pk = build_centered_binomial_law(ps.ke)        # LWE error law for the key
    # Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext
    # chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)  # LWE + rounding error ciphertext

    # B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B1 = law_product(chie_pk, chis)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D

def weak_key_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_centered_binomial_law(ps.ks)           # LWE error law for the key
    chie = build_centered_binomial_law(ps.ke_ct)        # LWE error law for the ciphertext
    chie_pk = build_centered_binomial_law(ps.ke)        # LWE error law for the key
    # Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext
    # chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)  # LWE + rounding error ciphertext

    # B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B1 = law_product(chie_pk, chis)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D

# SMY
def uni_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_law(ps.ks)           # LWE error law for the key
    # print(chis)
    chie = build_uniform_law(ps.ke_ct)        # LWE error law for the ciphertext
    # print(chie)
    chie_pk = build_uniform_law(ps.ke)
    # print(chie_pk)
    # Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key

    # par_round1 = round(ps.q/ ps.rqc)
    # Rc = build_uniform_law(par_round1)
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    print("rounding error first ciphertext", Rc)

    # chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)  # LWE + rounding error ciphertext

    # B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B1 = law_product(chie_pk, chis)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    print("ps.m, ps.n", ps.m, ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    # print("rounding error second ciphertext", R2)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D


# s,e,r,e_1,e_2分开采样er+s(e1+u1)+e2+u2
def uni_any_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_law(ps.ks)
    print("chis", chis)
    chie = build_uniform_law(ps.ke)
    print("chie", chie)
    chir = build_uniform_law(ps.kr)
    print("chir", chir)
    chie1 = build_uniform_law(ps.ke1)
    print("chie1", chie1)
    chie2 = build_uniform_law(ps.ke2)
    print("chie2", chie2)

    chiu1 = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    print("chiu1", chiu1)

    chie1_u1 = law_convolution(chie1, chiu1)  # e1+u1

    B1 = law_product(chie, chir)  # er
    B2 = law_product(chis, chie1_u1)  # s(e1+u1)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    chiu2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    print("chiu2", chiu2)
    F = law_convolution(chie2, chiu2)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D


# s,e,r,e_1,e_2分开采样er+s(e1+u1)+e2+u2
def cbd_any_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_centered_binomial_law(ps.ks)
    print("chis", chis)
    chie = build_centered_binomial_law(ps.ke)
    print("chie", chie)
    chir = build_centered_binomial_law(ps.kr)
    print("chir", chir)
    chie1 = build_centered_binomial_law(ps.ke1)
    print("chie1", chie1)
    chie2 = build_centered_binomial_law(ps.ke2)
    print("chie2", chie2)

    chiu1 = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    print("chiu1", chiu1)

    chie1_u1 = law_convolution(chie1, chiu1)  # e1+u1

    B1 = law_product(chie, chir)  # er
    B2 = law_product(chis, chie1_u1)  # s(e1+u1)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    chiu2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    print("chiu2", chiu2)
    F = law_convolution(chie2, chiu2)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D

# the uniform distribution [-k,k-1], 2k elements
def uni_short_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_short_law(ps.ks)           # LWE error law for the key
    print(chis)
    chie = build_uniform_short_law(ps.ke_ct)        # LWE error law for the ciphertext
    print(chie)
    chie_pk = build_uniform_short_law(ps.ke)
    print(chie_pk)
    # Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    print("rounding error first ciphertext", Rc)

    # chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)  # LWE + rounding error ciphertext

    # B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B1 = law_product(chie_pk, chis)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    print("rounding error second ciphertext", R2)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D


# s,e,r,e_1,e_2分开采样er+s(e1+u1)+e2+u2, [-k,k-1]
def uni_any_short_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_short_law(ps.ks)
    print("chis", chis)
    chie = build_uniform_law(ps.ke)
    print("chie", chie)
    chir = build_uniform_law(ps.kr)
    print("chir", chir)
    chie1 = build_uniform_law(ps.ke1)
    print("chie1", chie1)
    chie2 = build_uniform_short_law(ps.ke2)
    print("chie2", chie2)

    chiu1 = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    # print("chiu1", chiu1)

    chie1_u1 = law_convolution(chie1, chiu1)  # e1+u1
    # print("chie1_u1", chie1_u1)

    B1 = law_product(chie, chir)  # er
    B2 = law_product(chis, chie1_u1)  # s(e1+u1)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    chiu2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    # print("chiu2", chiu2)
    F = law_convolution(chie2, chiu2)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    # print("D", D)
    return D


# s,e,r,e_1,e_2分开采样er+s(e1+u1)+e2+u2, [-k,0)(0,k]
def uni_any_edge_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_edge_law(ps.ks)
    print("chis", chis)
    chie = build_uniform_edge_law(ps.ke)
    print("chie", chie)
    chir = build_uniform_edge_law(ps.kr)
    print("chir", chir)
    chie1 = build_uniform_edge_law(ps.ke1)
    print("chie1", chie1)
    chie2 = build_uniform_edge_law(ps.ke2)
    print("chie2", chie2)

    chiu1 = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    # print("chiu1", chiu1)

    chie1_u1 = law_convolution(chie1, chiu1)  # e1+u1
    # print("chie1_u1", chie1_u1)

    B1 = law_product(chie, chir)  # er
    B2 = law_product(chis, chie1_u1)  # s(e1+u1)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    chiu2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    # print("chiu2", chiu2)
    F = law_convolution(chie2, chiu2)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    # print("D", D)
    return D


# s,e,r,e_1,e_2分开采样er+s(e1+u1)+e2+u2, 采取不同的均匀分布采样方法
def uni_any_mix_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_law(ps.ks)
    print("chis", chis)
    chie = build_uniform_law(ps.ke)
    print("chie", chie)
    chir = build_uniform_law(ps.kr)
    print("chir", chir)
    chie1 = build_uniform_law(ps.ke1)
    print("chie1", chie1)
    chie2 = build_uniform_law(ps.ke2)
    print("chie2", chie2)

    chiu1 = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext
    # print("chiu1", chiu1)

    chie1_u1 = law_convolution(chie1, chiu1)  # e1+u1
    # print("chie1_u1", chie1_u1)

    B1 = law_product(chie, chir)  # er
    B2 = law_product(chis, chie1_u1)  # s(e1+u1)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    chiu2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    # print("chiu2", chiu2)
    F = law_convolution(chie2, chiu2)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    # print("D", D)
    return D

def CBD_Uni_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_centered_binomial_law(ps.ks)            # LWE error law for the key
    print(chis)
    chie = build_uniform_law(ps.ke_ct)        # LWE error law for the ciphertext
    print(chie)
    chie_pk = build_uniform_law(ps.ke)
    print(chie_pk)
    Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext
    chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)                   # LWE + rounding error ciphertext

    B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D


def Uni_CBD_p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_law(ps.ks)            # LWE error law for the key
    print(chis)
    chie = build_centered_binomial_law(ps.ke_ct)        # LWE error law for the ciphertext
    print(chie)
    chie_pk = build_centered_binomial_law(ps.ke)
    print(chie_pk)
    Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext
    chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)                   # LWE + rounding error ciphertext

    B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D
def p2_cyclotomic_error_probability(ps):
    # F = p2_cyclotomic_final_error_distribution(ps)
    F = uni_p2_cyclotomic_final_error_distribution(ps)
    # F = cbd_any_p2_cyclotomic_final_error_distribution(ps)
    # F = uni_any_p2_cyclotomic_final_error_distribution(ps)
    # F = uni_short_p2_cyclotomic_final_error_distribution(ps)
    # F = uni_any_short_p2_cyclotomic_final_error_distribution(ps)
    # F = uni_any_edge_p2_cyclotomic_final_error_distribution(ps)
    # F = uni_any_mix_p2_cyclotomic_final_error_distribution(ps)
    # F = CBD_Uni_p2_cyclotomic_final_error_distribution(ps)
    # F = Uni_CBD_p2_cyclotomic_final_error_distribution(ps)
    proba = tail_probability(F, ps.q/4)
    return F, ps.n*proba


def summarize(ps):
    print("params: ", ps.__dict__)
    F, f = p2_cyclotomic_error_probability(ps)
    print("failure: %.1f = 2^%.1f"%(f, log(f + 2.**(-300))/log(2)))


if __name__ == "__main__":
    # Parameter sets
    ps_light = KyberParameterSet(256, 2, 3, 3, 3329, 2 ** 12, 2 ** 10, 2 ** 4, ke_ct=2)
    ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2 ** 12, 2 ** 10, 2 ** 4)
    ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2 ** 12, 2 ** 11, 2 ** 5)

    # Analyses
    print("Kyber512 (light):")
    print("--------------------")
    summarize(ps_light)
    print()

    print("Kyber768 (recommended):")
    print("--------------------")
    summarize(ps_recommended)
    print()

    print("Kyber1024 (paranoid):")
    print("--------------------")
    summarize(ps_paranoid)
    print()
