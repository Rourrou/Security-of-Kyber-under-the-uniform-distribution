from proba_util import *


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


def encryption_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_centered_binomial_law(ps.ks)           # LWE error law for the key
    chie = build_centered_binomial_law(ps.ke_ct)        # LWE error law for the ciphertext
    chie_pk = build_centered_binomial_law(ps.ke)        # LWE error law for the key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext
    chiRe = law_convolution(chie, Rc)  # LWE + rounding error ciphertext

    B1 = law_product(chie_pk, chis)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error

    proba = tail_probability(D, ps.q / 4)
    return D, ps.n * proba
    return D


def uni_encryption_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = build_uniform_law(ps.ks)           # LWE error law for the key
    chie = build_uniform_law(ps.ke_ct)        # LWE error law for the ciphertext
    chie_pk = build_uniform_law(ps.ke)

    Rc = build_mod_switching_error_law(ps.q, ps.rqc)  # rounding error first ciphertext

    chiRe = law_convolution(chie, Rc)  # LWE + rounding error ciphertext

    B1 = law_product(chie_pk, chis)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C = law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error

    proba = tail_probability(D, ps.q / 4)
    return D, ps.n*proba



def failure(ps):
    print("params: ", ps.__dict__)
    # compute the decryption failure probability of Kyber
    F, f = encryption_error_distribution(ps)
    print("Kyber's decryption failure probability = 2^%.1f" % (log(f + 2. ** (-300)) / log(2)))

    # compute the decryption failure probability of the variant of Kyber under the uniform distribution
    G, g = uni_encryption_error_distribution(ps)
    print("Variant of Kyber under the uniform distribution's decryption failure probability = 2^%.1f"%(log(g + 2.**(-300))/log(2)))


if __name__ == "__main__":
    # Parameter sets
    ps_light = KyberParameterSet(256, 2, 3, 3, 3329, 2 ** 12, 2 ** 10, 2 ** 4, ke_ct=2)
    ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2 ** 12, 2 ** 10, 2 ** 4)
    ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2 ** 12, 2 ** 11, 2 ** 5)

    # Analyses
    print("Kyber512 (light):")
    print("--------------------")
    failure(ps_light)
    print()

    print("Kyber768 (recommended):")
    print("--------------------")
    failure(ps_recommended)
    print()

    print("Kyber1024 (paranoid):")
    print("--------------------")
    failure(ps_paranoid)
    print()
