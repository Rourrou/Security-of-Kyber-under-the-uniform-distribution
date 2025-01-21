from math import log
from Kyber_failure import p2_cyclotomic_error_probability
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet, MLWE_optimize_attack
from proba_util import build_mod_switching_error_law

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


def Kyber_to_MLWE(kps):
    if kps.ks != kps.ke:
        raise "The security script does not handle different error parameter in secrets and errors (ks != ke) "

    # Check whether ciphertext error variance after rounding is larger than secret key error variance
    Rc = build_mod_switching_error_law(kps.q, kps.rqc)
    var_rounding = sum([i*i*Rc[i] for i in Rc.keys()])

    if kps.ke_ct/2. + var_rounding < kps.ke/2.:
        raise "The security of the ciphertext MLWE may not be stronger than the one of the public key MLWE"

    return MLWEParameterSet(kps.n, kps.m, kps.m + 1, kps.ks, kps.q)


def communication_costs(ps):
    """ Compute the communication cost of a parameter set
    :param ps: Parameter set (ParameterSet)
    :returns: (cost_Alice, cost_Bob) (in Bytes)
    """
    A_space = 256 + ps.n * ps.m * log(ps.rqk)/log(2)
    B_space = ps.n * ps.m * log(ps.rqc)/log(2) + ps.n * log(ps.rq2)/log(2)
    return (int(round(A_space))/8., int(round(B_space))/8.)


def summarize(ps):
    print ("params: ", ps.__dict__)
    print ("com costs: ", communication_costs(ps))
    F, f = p2_cyclotomic_error_probability(ps)
    index = log(f + 2.**(-300))/log(2)
    print ("failure: %.1f = 2^%.1f"%(f, log(f + 2.**(-300))/log(2)))
    return index



if __name__ == "__main__":
    # Parameter sets
    eta_list = []
    kyber512_fail = []
    kyber512_security = []
    kyber768_fail = []
    kyber768_security = []
    kyber1024_fail = []
    kyber1024_security = []

    for eta in range(1,4,1):
        for du in range(7,12,1):
            for dv in range(3,12,1):
                eta_list.append(eta)
                ps_light = KyberParameterSet(256, 2, eta, eta, 3329, 2 ** 12, 2 ** du, 2 ** dv)
                ps_recommended = KyberParameterSet(256, 3, eta, eta, 3329, 2 ** 12, 2 ** du, 2 ** dv)
                ps_paranoid = KyberParameterSet(256, 4, eta, eta, 3329, 2 ** 12, 2 ** du, 2 ** dv)

                print("eta = %d, du = %d, dv = %d" % (eta, du, dv))

                # # Analyses
                # print ("Kyber512 (light):")
                # print ("--------------------")
                # print ("security:")
                # b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps_light))
                # kyber512_security.append(c_pc)
                # fail_index = summarize(ps_light)
                # kyber512_fail.append(fail_index)
                # print ()
                #
                print ("Kyber768 (recommended):")
                print ("--------------------")
                print ("security:")
                b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps_recommended))
                kyber768_security.append(c_pc)
                fail_index = summarize(ps_recommended)
                kyber768_fail.append(fail_index)
                # # print ()
                # #
                # print ("Kyber1024 (paranoid):")
                # print ("--------------------")
                # print ("security:")
                # b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps_paranoid))
                # kyber1024_security.append(c_pc)
                # fail_index = summarize(ps_paranoid)
                # kyber1024_fail.append(fail_index)
                # # print ()
    print("eta =", eta_list)
    # print("kyber512_fail =", kyber512_fail)
    # print("kyber512_security =", kyber512_security)
    print("kyber768_fail =", kyber768_fail)
    print("kyber768_security =", kyber768_security)
    # print("kyber1024_fail =", kyber1024_fail)
    # print("kyber1024_security =", kyber1024_security)