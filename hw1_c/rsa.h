#ifndef RSA_H
#define RSA_H

#include <gmp.h>

mpz_t *encrypt( mpz_t *, int, mpz_t, mpz_t );
mpz_t *decrypt( mpz_t *, int, mpz_t, mpz_t );

void expmod( mpz_t, mpz_t, mpz_t, mpz_t );
void expmod_rabin( mpz_t, mpz_t, mpz_t, mpz_t );

int is_prime( mpz_t );
int is_even( mpz_t );

#endif
