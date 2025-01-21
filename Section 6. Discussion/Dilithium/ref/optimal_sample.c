#include "optimal_sample.h"
#include "symmetric.h"

#define UDILITHIUM_PRFBYTES_U2 84 + 136 - 1
#define UDILITHIUM_PRFBYTES_U2_NBLOCKS 1
#define UDILITHIUM_PRFBYTES_U4 112 + 136 - 1
#define UDILITHIUM_PRFBYTES_U4_NBLOCKS 1

// [-4, 4], need 16 bits for 5 samples.
static unsigned int rej_uniform_u4(int32_t *a, unsigned int len,
                                   const uint8_t *buf, unsigned int buflen) {
  unsigned int ctr, pos;
  uint16_t val;
  int q, r0;

  ctr = pos = 0;
  while (pos < UDILITHIUM_PRFBYTES_U4) {
    // load 16 bits
    unsigned int val;
    val = buf[pos++];
    val = val << 8;
    val += buf[pos++];

    // sample 5 coeffs
    if (val < 59049) {
      for (int j = 0; j < 5; j++) {
        q = val / 9;
        r0 = val - 9 * q;
        val = q;

        a[ctr++] = r0 - 4;
        if (ctr == N) {
          return ctr;
        }
      }
    }
  }

  return ctr;
}

// [-2, 2], need 7 bits for 3 samples.
static unsigned int rej_uniform_u2(int32_t *a, unsigned int len,
                                   const uint8_t *buf, unsigned int buflen) {
  unsigned int ctr, pos;
  uint16_t val;
  int q, r0;

  ctr = pos = 0;
  while (ctr < len && pos < buflen) {
    // load 7 bits
    val = buf[pos++];
    val = val >> 1;

    // sample 3 coeffs
    if (val < 125) {
      for (int j = 0; j < 3; j++) {
        q = val / 5;
        r0 = val - 5 * q;
        val = q;

        a[ctr++] = r0 - 2;
        if (ctr == N) {
          return ctr;
        }
      }
    }
  }
  return ctr;
}

void poly_uniform_u2(poly *r, const uint8_t seed[CRHBYTES], uint16_t nonce) {
  unsigned int ctr;
  unsigned int buflen = UDILITHIUM_PRFBYTES_U2_NBLOCKS * STREAM256_BLOCKBYTES;
  uint8_t buf[UDILITHIUM_PRFBYTES_U2_NBLOCKS * STREAM256_BLOCKBYTES];
  stream256_state state;

  stream256_init(&state, seed, nonce);
  stream256_squeezeblocks(buf, UDILITHIUM_PRFBYTES_U2_NBLOCKS, &state);

  ctr = rej_uniform_u2(r->coeffs, N, buf, buflen);

  while (ctr < N) {
    stream256_squeezeblocks(buf, 1, &state);
    ctr += rej_uniform_u2(r->coeffs + ctr, N - ctr, buf, STREAM256_BLOCKBYTES);
  }
}

void poly_uniform_u4(poly *r, const uint8_t seed[CRHBYTES], uint16_t nonce) {
  unsigned int ctr;
  unsigned int buflen = UDILITHIUM_PRFBYTES_U4_NBLOCKS * STREAM256_BLOCKBYTES;
  uint8_t buf[UDILITHIUM_PRFBYTES_U4_NBLOCKS * STREAM256_BLOCKBYTES];
  stream256_state state;

  stream256_init(&state, seed, nonce);
  stream256_squeezeblocks(buf, UDILITHIUM_PRFBYTES_U4_NBLOCKS, &state);

  ctr = rej_uniform_u4(r->coeffs, N, buf, buflen);

  while (ctr < N) {
    stream256_squeezeblocks(buf, 1, &state);
    ctr += rej_uniform_u4(r->coeffs + ctr, N - ctr, buf, STREAM256_BLOCKBYTES);
  }
}
