#include <stdlib.h>
#include <time.h>
#include <gmp.h>
#include "rsa.h"

int is_even( mpz_t );

/* encryption of message m
 * uses chinese remainder theorem
 */
mpz_t *encrypt( mpz_t *m, int l, mpz_t e, mpz_t n )
{
	mpz_t *c = malloc( sizeof(mpz_t) * l );
	return c;
}

/* decryption of cipher c
 * uses chinese remainder theorem
 */
mpz_t *decrypt( mpz_t *c, int l, mpz_t d, mpz_t n )
{
	mpz_t *m = malloc( sizeof(mpz_t) * l );
	return m;
}

/* fast expmod for mpz_t */
void expmod( mpz_t v, mpz_t a, mpz_t b, mpz_t n )
{
	if( !mpz_cmp_ui( b, 0 ) )
		mpz_set( v, 1 );

	while( mpz_cmp_ui( b, 0 ) )
	{
		if( is_even(b) )
		{
			mpz_mul( a, a, a ); // a^2
			mpz_mod( a, a, n ); // a % n
			mpz_fdiv_q_ui( b, b, 2 ); // b//2 
		}
		else
		{
			mpz_sub_ui( b, b, 1 );
			mpz_mul( v, v, a );
			mpz_mod( v, v, n );
		}
	}
}

/* expmod but with Rabin test implanted */
void expmod_rabin( mpz_t z, mpz_t a, mpz_t b, mpz_t n )
{
	if( !mpz_cmp_ui( b, 0 ) )
		mpz_set( z, 1 )

	while( mpz_cmp_ui( b, 0 ) )
	{
		if( is_even(b) )
		{
			mpz_mul( z, a, a ) // z = a^2
			mpz_mod( a, a, n ); // a % n
			mpz_fdiv_q_ui( b, b, 2 ); // b//2 
			// Miller Rabin test
		}
		else
		{
			mpz_sub_ui( b, b, 1 );
			mpz_mul( z, z, a );
			mpz_mod( z, z, n );
		}
	}
}

/* checks primality of mpz_t 
 * uses Miller test with Rabin implanted inside
 */
int is_prime( mpz_t p, int L )
{
	assert( !is_even(p) );

	for( int i = 0; i < L; i++ )
	{
		gmp_randstate_t r;
		gmp_randinit_mt(r);
		mpz_t a;
		mpz_sub_ui( p, p, 1 );
		mpz_urandomm( a, r, p ); // a = 0->p-2
		mpz_add_ui( a, a, 1 ); // a = 1->p-1
		mpz_add_ui( p, p, 1 );
		
		expmod_rabin( 
	}
}

/* checks if mpz_t is even */
int is_even( mpz_t a )
{
	mpz_mod_ui( a, a, 2 )
	return !a;
}
