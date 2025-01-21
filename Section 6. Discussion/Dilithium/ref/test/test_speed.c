#include "../optimal_sample.h"
#include "../params.h"
#include "../poly.h"
#include "../polyvec.h"
#include "../sign.h"
#include "cpucycles.h"
#include "speed_print.h"
#include <stdint.h>
#include <stdio.h>

#define NTESTS 10000

uint64_t t[NTESTS];

int main(void) {
  unsigned int i;
  size_t siglen;
  uint8_t pk[CRYPTO_PUBLICKEYBYTES];
  uint8_t sk[CRYPTO_SECRETKEYBYTES];
  uint8_t sig[CRYPTO_BYTES];
  uint8_t seed[CRHBYTES];
  polyvecl mat[K];
  poly *a = &mat[0].vec[0];
  poly *b = &mat[0].vec[1];
  poly *c = &mat[0].vec[2];

  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    polyvec_matrix_expand(mat, seed);
  }
  // print_results("polyvec_matrix_expand:", t, NTESTS);
  // printf("\n\n");

#if DILITHIUM_MODE == 3
  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_uniform_u4(a, seed, 0);
  }
  print_results("poly_uniform_u4:", t, NTESTS);
#endif

#if DILITHIUM_MODE == 2 || DILITHIUM_MODE == 5
  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_uniform_u2(a, seed, 0);
  }
  print_results("poly_uniform_u2:", t, NTESTS);
#endif

  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_uniform_eta(a, seed, 0);
  }
  print_results("poly_uniform_eta:", t, NTESTS);

  /*
  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_uniform_gamma1(a, seed, 0);
  }
  print_results("poly_uniform_gamma1:", t, NTESTS);

  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_ntt(a);
  }
  print_results("poly_ntt:", t, NTESTS);

  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_invntt_tomont(a);
  }
  print_results("poly_invntt_tomont:", t, NTESTS);

  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_pointwise_montgomery(c, a, b);
  }
  print_results("poly_pointwise_montgomery:", t, NTESTS);

  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    poly_challenge(c, seed);
  }
  print_results("poly_challenge:", t, NTESTS);
  */

  /* Sample short vectors s1 and s2 */
  polyvecl s1;
  polyveck s2;
  uint8_t rhoprime[CRHBYTES];

  printf("\n");
#if DILITHIUM_MODE == 3
  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    polyvecl_uniform_u4(&s1, rhoprime, 0);
    polyveck_uniform_u4(&s2, rhoprime, L);
  }
  print_results("polyvec_u4_s1s2:", t, NTESTS);
#endif

#if DILITHIUM_MODE == 2 || DILITHIUM_MODE == 5
  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    polyvecl_uniform_u2(&s1, rhoprime, 0);
    polyveck_uniform_u2(&s2, rhoprime, L);
  }
  print_results("polyvec_u2_s1s2:", t, NTESTS);
#endif

  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    polyvecl_uniform_eta(&s1, rhoprime, 0);
    polyveck_uniform_eta(&s2, rhoprime, L);
  }
  print_results("polyvec_eta_s1s2:", t, NTESTS);

  printf("\n");
#if DILITHIUM_MODE == 3
  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    crypto_sign_keypair_u4(pk, sk);
  }
  print_results("Keypair_u4:", t, NTESTS);
#endif

#if DILITHIUM_MODE == 2 || DILITHIUM_MODE == 5
  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    crypto_sign_keypair_u2(pk, sk);
  }
  print_results("Keypair_u2:", t, NTESTS);
#endif

  for (i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    crypto_sign_keypair(pk, sk);
  }
  print_results("Keypair:", t, NTESTS);

  /*
  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    crypto_sign_signature(sig, &siglen, sig, CRHBYTES, sk);
  }
  print_results("Sign:", t, NTESTS);

  for(i = 0; i < NTESTS; ++i) {
    t[i] = cpucycles();
    crypto_sign_verify(sig, CRYPTO_BYTES, sig, CRHBYTES, pk);
  }
  print_results("Verify:", t, NTESTS);
  */

  return 0;
}
