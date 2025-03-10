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


if __name__ == "__main__":
    # Parameter sets
    ps_toy1 = KyberParameterSet(128, 1, 3, 3, 3329, 2 ** 12, 2 ** 10, 2 ** 4)
    ps_light = KyberParameterSet(256, 2, 3, 3, 3329, 2 ** 12, 2 ** 10, 2 ** 4, ke_ct=2)
    ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2 ** 12, 2 ** 10, 2 ** 4)
    ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2 ** 12, 2 ** 11, 2 ** 5)

    # Analyses
    # print("Kyber128 (toy1):")
    # print("--------------------")
    # print("security:")
    # MLWE_summarize_attacks(Kyber_to_MLWE(ps_toy1))
    # print()

    print("Kyber512 (light):")
    print("--------------------")
    print("security:")
    MLWE_summarize_attacks(Kyber_to_MLWE(ps_light))
    print()
    #
    # print("Kyber768 (recommended):")
    # print("--------------------")
    # print("security:")
    # MLWE_summarize_attacks(Kyber_to_MLWE(ps_recommended))
    # print()
    #
    # print("Kyber1024 (paranoid):")
    # print("--------------------")
    # print("security:")
    # MLWE_summarize_attacks(Kyber_to_MLWE(ps_paranoid))
    # print()
