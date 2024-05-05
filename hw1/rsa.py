from helpers import *
from random import getrandbits as randbits, randint

if __name__ == '__main__':
    # random 4096-bit primes
    k = 4096
    p = randbits(k)
    while not is_prime(p):
        p = randbits(k)
    print( 'found prime p' )
    q = randbits(k)
    while (q == p) or not is_prime(q):
        q = randbits(k)
    print( 'found prime q' )

    # p < q
    if p > q:
        p ^= q
        q ^= p
        p ^= q

    # n and euler totient
    n = p*q
    phi = (p-1)*(q-1)

    # find secret e and compute d
    e = randint( 3, phi )
    _, d = xgcd( phi, e )
    while is_even(e) or ((d*e) % phi) != 1:
        e = randint( 3, phi )
        _, d = xgcd( phi, e )
    while d < 0:
        d += phi

    print( 'found e, d' )

    # not required, but e < d
    if e > d:
        e ^= d
        d ^= e
        e ^= d
        
    # open plaintext and re-encrypt
    plaintext = open( 'a1.plaintext', 'r' ).readlines()
    encryption = open( 'a1.encrypted', 'w' )
    for line in plaintext:
        for char in line:
            encryption.write( str(rsa_encrypt( ord(char), e, n )) + '\n' )

    # write secret keys to file
    keys = open( 'a1.privkeys', 'w' )
    keys.write( str(n) + '\n' )
    keys.write( str(e) + '\n' )
    keys.write( str(d) )
