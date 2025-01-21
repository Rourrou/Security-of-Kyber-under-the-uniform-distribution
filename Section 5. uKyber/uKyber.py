from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet
from proba_util import *

class KyberParameterSet:
    def __init__(self, n, m, ks, ke, kr, ke1, ke2, q, rqk, rqc, rq2):
        self.n = n
        self.m = m
        self.ks = ks     # binary distribution for the secret key
        self.ke = ke    # binary distribution for the ciphertext errors
        self.kr = kr    # binary distribution for the ciphertext errors
        self.ke1 = ke1
        self.ke2 = ke2
        self.q = q
        self.rqk = rqk  # 2^(bits in the public key)
        self.rqc = rqc  # 2^(bits in the first ciphertext)
        self.rq2 = rq2  # 2^(bits in the second ciphertext)


def Kyber_to_MLWE(kps):
    # if kps.ks != kps.ke:
    #     raise "The security script does not handle different error parameter in secrets and errors (ks != ke) "

    # Check whether ciphertext error variance after rounding is larger than secret key error variance
    Rc = build_mod_switching_error_law(kps.q, kps.rqc)
    var_rounding = sum([i*i*Rc[i] for i in Rc.keys()])
    print("var_rounding", var_rounding)

    # if kps.ke1/2. + var_rounding < kps.ke/2.:
    #     # print("var_rounding", var_rounding)
    #     raise "The security of the ciphertext MLWE may not be stronger than the one of the public key MLWE"

    # if ((2 * kps.ke1) ^ 2 - 1) / 2 + var_rounding < ((2 * kps.ke) ^ 2 - 1) / 2:
    #     raise "The security of the ciphertext MLWE may not be stronger than the one of the public key MLWE"

    return MLWEParameterSet(kps.n, kps.m, kps.m + 1, kps.ks, kps.q)


def communication_costs(ps):
    """ Compute the communication cost of a parameter set
    :param ps: Parameter set (ParameterSet)
    :returns: (cost_Alice, cost_Bob) (in Bytes)
    """
    A_space = 256 + ps.n * ps.m * log(ps.rqk)/log(2)
    B_space = ps.n * ps.m * log(ps.rqc)/log(2) + ps.n * log(ps.rq2)/log(2)
    return (int(round(A_space))/8., int(round(B_space))/8.)


def p2_cyclotomic_error_probability(ps):
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

    chiu2 = build_mod_switching_error_law(ps.q, ps.rq2)  # Rounding2 (in the ciphertext mask part)
    print("chiu2", chiu2)
    F = law_convolution(chie2, chiu2)  # LWE+Rounding2 error
    D = law_convolution(C, F)  # Final error
    proba = tail_probability(D, ps.q/4)
    return D, ps.n*proba

def summarize(ps):
    print ("params: ", ps.__dict__)
    print ("com costs: ", communication_costs(ps))
    F, f = p2_cyclotomic_error_probability(ps)
    print ("failure: %.1f = 2^%.1f"%(f, log(f + 2.**(-300))/log(2)))


if __name__ == "__main__":
    # Parameter sets
    # n, m, ks, ke, kr, ke1, ke2, q, rqk, rqc, rq2
    # uniform
    ps_light = KyberParameterSet(256, 2, 1, 2, 1, 1, 1, 3329, 2 ** 12, 2 ** 9, 2 ** 3)
    ps_recommended = KyberParameterSet(256, 3, 1, 2, 1, 1, 1, 3329, 2 ** 12, 2 ** 10, 2 ** 3)
    ps_paranoid = KyberParameterSet(256, 4, 1, 2, 1, 1, 1, 3329, 2 ** 12, 2 ** 10, 2 ** 5)

    # Analyses
    print ("Kyber512 (light):")
    print ("--------------------")
    print ("security:")
    MLWE_summarize_attacks(Kyber_to_MLWE(ps_light))
    summarize(ps_light)
    print ()
    # #
    print ("Kyber768 (recommended):")
    print ("--------------------")
    print ("security:")
    MLWE_summarize_attacks(Kyber_to_MLWE(ps_recommended))
    summarize(ps_recommended)
    print ()

    print ("Kyber1024 (paranoid):")
    print ("--------------------")
    print ("security:")
    MLWE_summarize_attacks(Kyber_to_MLWE(ps_paranoid))
    summarize(ps_paranoid)
    print ()
