#include "params.h"
#include "poly.h"
#include "symmetric.h"
#include <stdint.h>


void poly_getnoise_u1(poly *r, const uint8_t seed[KYBER_SYMBYTES],
                      uint8_t nonce);
void poly_getnoise_u2(poly *r, const uint8_t seed[KYBER_SYMBYTES],
                      uint8_t nonce);

int poly_getnoise_u1k(poly *r, uint8_t *buf);
int poly_getnoise_u2k(poly *r, uint8_t *buf);
