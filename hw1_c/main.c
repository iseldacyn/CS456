#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <gmp.h>
#include "rsa.h"

/* read functions */
void read_cipher( FILE *, mpz_t * );
void read_pubkeys( FILE *, mpz_t, mpz_t );

/* main function */
int main()
{
	// read in message from file
	FILE *cipher = fopen( "a1.cipher", "r" );

	return 0;
}
