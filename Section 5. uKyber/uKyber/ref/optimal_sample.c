#include "optimal_sample.h"
#include <stdio.h>

#define UKYBER_PRFBYTES_NOTHING 128

void bytes_to_bits(uint8_t bits[UKYBER_PRFBYTES_NOTHING * 8],
                   const uint8_t bytes[UKYBER_PRFBYTES_NOTHING]) {
  int byte;
  for (int j = 0; j < UKYBER_PRFBYTES_NOTHING; j++) {
    byte = bytes[j];
    for (int z = 7; z >= 0; z--) {
      bits[j * 8 + 7 - z] = (byte & (0x01 << z)) == (0x01 << z) ? 1 : 0;
    }
  }
}

// [-1, 1], need 8 bits for 5 samples.
static unsigned int poly_rej_uniform_u1(poly *r, const uint8_t *buf) {
  unsigned int ctr, pos;

  ctr = pos = 0;
  uint16_t val = 0;
  while (ctr < KYBER_N - 1) {
    val = buf[pos++];
    if (val >= 243)
      continue;

    /*
    if (pos > UKYBER_PRFBYTES) {
      printf("no space!!!!!\n");
    }
    */

    // sample 5 coeffs
    r->coeffs[ctr++] = val % 3 - 1;
    r->coeffs[ctr++] = (val / 3) % 3 - 1;
    r->coeffs[ctr++] = (val / 9) % 3 - 1;
    r->coeffs[ctr++] = (val / 27) % 3 - 1;
    r->coeffs[ctr++] = (val / 81) % 3 - 1;
  }
  r->coeffs[ctr] = buf[pos] % 3 - 1;

  // return ctr;
  return pos;
}

// [-2, 2], need 7 bits for 3 samples.
static unsigned int poly_rej_uniform_u2_optimal(poly *r, const uint8_t *buf) {
  unsigned int ctr, pos;
  uint16_t val;

  ctr = pos = 0;
  int q, r0;

  while (ctr < KYBER_N - 1) {
    val = buf[pos++] >> 1;
    if (val >= 125)
      continue;

    /*
    if (pos > UKYBER_PRFBYTES) {
      printf("no space!!!!!\n");
    }
    */

    // 3 samples.
    for (int j = 0; j < 3; j++) {
      q = val / 5;
      r0 = val - 5 * q;
      val = q;

      r->coeffs[ctr++] = r0 - 2;
    }
  }

  r->coeffs[ctr] = buf[pos] % 5 - 2;

  // return ctr;
  return pos;
}

// [-2, 2], need 7 bits for 3 samples.
static unsigned int
poly_rej_uniform_u2(poly *r, const uint8_t buf[UKYBER_PRFBYTES_NOTHING]) {
  unsigned int ctr, pos;
  uint16_t val;
  int q, r0;
  uint8_t bits4buf[UKYBER_PRFBYTES_NOTHING * 8];

  bytes_to_bits(bits4buf, buf);

  ctr = pos = 0;
  while (pos < sizeof bits4buf) {
    // load 7 bits
    val = 0;
    for (int j = 0; j < 7; j++) {
      val += bits4buf[pos + j] << (6 - j);
    }
    pos += 7;

    // sample 3 coeffs
    if (val < 125) {
      for (int j = 0; j < 3; j++) {
        q = val / 5;
        r0 = val - 5 * q;
        val = q;

        r->coeffs[ctr++] = r0 - 2;
        if (ctr == KYBER_N)
          return ctr;
      }
    }
  }

  return ctr;
}
void poly_getnoise_u2(poly *r, const uint8_t seed[KYBER_SYMBYTES],
                      uint8_t nonce) {
  uint8_t buf[UKYBER_PRFBYTES_NOTHING];
  prf(buf, sizeof(buf), seed, nonce);
  // poly_rej_uniform_u2(r, buf);
  poly_rej_uniform_u2_optimal(r, buf);
}

void poly_getnoise_u1(poly *r, const uint8_t seed[KYBER_SYMBYTES],
                      uint8_t nonce) {
  uint8_t buf[UKYBER_PRFBYTES_NOTHING];
  prf(buf, sizeof(buf), seed, nonce);
  poly_rej_uniform_u1(r, buf);
}

int poly_getnoise_u1k(poly *r, uint8_t *buf) {
  return poly_rej_uniform_u1(r, buf);
}

int poly_getnoise_u2k(poly *r, uint8_t *buf) {
  return poly_rej_uniform_u2_optimal(r, buf);
}

/*
int maixn() {
  poly s;
  uint8_t seed[KYBER_SYMBYTES];
  uint8_t nonce;
  poly_getnoise_u2(&s, seed, nonce);
  for (int i = 0; i < 256; i++) {
    printf("%d ", s.coeffs[i]);
  }
  printf("\n");

  return 0;
}
*/
