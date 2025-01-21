from math import *
import functools

log_infinity = 9999

def delta_BKZ(b):
    """ The root hermite factor delta of BKZ-b
    """
    small = {0: 1e20, 1: 1e20, 2: 1.021900, 3: 1.020807, 4: 1.019713, 5: 1.018620,
             6: 1.018128, 7: 1.017636, 8: 1.017144, 9: 1.016652, 10: 1.016160,
             11: 1.015898, 12: 1.015636, 13: 1.015374, 14: 1.015112, 15: 1.014850,
             16: 1.014720, 17: 1.014590, 18: 1.014460, 19: 1.014330, 20: 1.014200,
             21: 1.014044, 22: 1.013888, 23: 1.013732, 24: 1.013576, 25: 1.013420,
             26: 1.013383, 27: 1.013347, 28: 1.013310, 29: 1.013253, 30: 1.013197,
             31: 1.013140, 32: 1.013084, 33: 1.013027, 34: 1.012970, 35: 1.012914,
             36: 1.012857, 37: 1.012801, 38: 1.012744, 39: 1.012687, 40: 1.012631,
             41: 1.012574, 42: 1.012518, 43: 1.012461, 44: 1.012404, 45: 1.012348,
             46: 1.012291, 47: 1.012235, 48: 1.012178, 49: 1.012121, 50: 1.012065}

    if b < 50:
        return small[b]
    else:
        delta = ((pi*b)**(1./b) * b / (2*pi*exp(1)))**(1./(2.*b-2.))
        return delta


def svp_plausible(b):
    """ log_2 of best plausible Quantum Cost of SVP in dimension b
    """
    return b *log(sqrt(4./3))/log(2)   # .2075 * b


def svp_quantum(b):
    """ log_2 of best plausible Quantum Cost of SVP in dimension b
    """
    return b *log(sqrt(13./9))/log(2)   # .265 * b  [Laarhoven Thesis]


def svp_classical(b):
    """ log_2 of best known Quantum Cost of SVP in dimension b
    """
    return b *log(sqrt(3./2))/log(2)    # .292 * b [Becker Ducas Laarhoven Gama]


def nvec_sieve(b):
    """ Number of short vectors outputted by a sieve step of blocksize b
    """
    return b *log(sqrt(4./3))/log(2)    # .2075 * b


## Adding Memoization to this really slow function
# @functools.lru_cache(maxsize=2**20)
def construct_BKZ_shape(q, nq, n1, b):
    """ Simulate the (log) shape of a basis after the reduction of
        a [q ... q, 1 ... 1] shape after BKZ-b reduction (nq many q's, n1 many 1's)
        This is implemented by constructing a longer shape and looking
        for the subshape with the right volume. Also outputs the index of the
        first vector <q, and the last >q.

        # Note: this implentation takes O(n). It is possible to output
        # a compressed description of the shape in time O(1), but it is much
        # more prone to making mistakes

    """
    d = nq+n1
    if b==0:
        L = nq*[log(q)] + n1*[0]
        return (nq, nq, L)


    slope = -2 * log(delta_BKZ(b))
    lq = log(q)
    B = int(floor(log(q) / - slope))    # Number of vectors in the sloppy region
    L = nq*[log(q)] + [lq + i * slope for i in range(1, B+1)] + n1*[0]

    x = 0
    lv = sum (L[:d])
    glv = nq*lq                     # Goal log volume

    while lv > glv:                 # While the current volume exceeeds goal volume, slide the window to the right
        lv -= L[x]
        lv += L[x+d]
        x += 1

    assert x <= B                   # Sanity check that we have not gone too far

    L = L[x:x+d]
    a = max(0, nq - x)             # The length of the [q, ... q] sequence
    B = min(B, d - a)              # The length of the GSA sequence

    diff = glv - lv
    assert abs(diff) < lq               # Sanity check the volume, up to the discretness of index error
    for i in range(a, a+B):        # Small shift of the GSA sequence to equiliBrate volume
        L[i] += diff / B
    lv = sum(L)
    assert abs(lv/glv - 1) < 1e-6        # Sanity check the volume

    return (a, a + B, L)


def construct_BKZ_shape_randomized(q, nq, n1, b):
    """ Simulate the (log) shape of a basis after the reduction of
        a [q ... q, 1 ... 1] shape after a randomization and a BKZ-b reduction
        (such that no GS vectors gets smaller than 1)
    """
    glv = nq * log(q)
    d = nq+n1
    L = []

    slope = -2 * log(delta_BKZ(b))
    li = 0
    lv = 0
    for i in range(d):
        li -= slope
        lv += li
        if lv>glv:
            break
        L = [li]+L
    B = len(L)                  # The length of the sloppy sequence
    L += (d-B)*[0]
    a = 0                        # The length of the [q, ... q] sequence

    lv = sum(L)
    diff = lv - glv
    #print diff, li
    #assert abs(diff) < li          # Sanity check the volume, up to the discretness of index error
    for i in range(a, a+B):        # Small shift of the GSA sequence to equiliBrate volume
        L[i] -= diff / B
    lv = sum(L)
    assert abs(lv/glv - 1) < 1e-6        # Sanity check the volume

    return (a, a + B, L)


def BKZ_first_length(q, nq, n1, b):
    """ Simulate the length of the shortest expected vector in the first b-block
        after randomization (killong q-vectors) and a BKZ-b reduction.
    """

    (_, _, L) = construct_BKZ_shape_randomized(q, nq, n1, b)
    l = exp(L[0])                # Compute the root-volume of the first block
    return l


def BKZ_last_block_length(q, nq, n1, b):
    """ Simulate the length of the expected Gram-Schmidt vector at position d-b (d = n+m)
        after a BKZ-b reduction.
    """

    (_, _, L) = construct_BKZ_shape(q, nq, n1, b)
    return exp(L[nq + n1 - b])

