from random import randint as rand

# miller-rabin primality test
def is_prime( m ):
    for i in range(20): # 1/2 ^ 20 < 1x10^-6
        a = rand( 1, m-1 )
        if expmod( a, m, m) != a :
            return 0
    return 1

# pulverizer of aryabhata, a>b
def xgcd( a, b ):
    q, r = a // b, a % b
    x1, y1 = 1, 0
    x2, y2 = 0, 1
    while r != 0:
        a, b = b, r
        tx, ty = x1, y1
        x1, y1 = x2, y2
        x2, y2 = tx - q*x2, ty - q*y2
        q, r = a // b, a % b
    return x1, y2

# fast looped exp % n
def expmod( a, b, n ):
    v = 1
    while b != 0:
        if is_even(b):
            a = square(a) % n
            b = b//2
        else:
            b -= 1
            v = (v*a) % n
    return v

def is_even( a ):
    return (a+1) % 2

def square( a ):
    return a * a

# generate public and secret keys for RSA
def gen_keys( k ):
   # random k-bit primes
    p = rand( 2**(k-1), 2**(k)-1 )
    while not is_prime(p):
        p = rand( 2**(k-1), 2**k-1 )

    q = rand( 2**(k-1), 2**(k)-1 )
    while (q == p) or not is_prime(q):
        q = rand( 2**(k-1), 2**k-1 )

    # p < q
    if p > q:
        p ^= q
        q ^= p
        p ^= q

    # n and euler totient
    n = p*q
    phi = (p-1)*(q-1)

    # generate an e until one works
    e = 3
    _, d = xgcd( phi, e )
    while ((e*d)%phi) != 1:
        e += 2
        _, d = xgcd( phi, e )
    while d < 0:
        d += phi

    # not required, but e < d
    if e > d:
        e ^= d
        d ^= e
        e ^= d

    return {"n": n, "e": e, "d": d, }

# class for RSA implementation
class RSA:
    def __init__( self, n, e, d ):
        self.n = n
        self.e = e
        self.d = d

    def generate(k):
        keys = gen_keys(k)
        return RSA( keys["n"], keys["e"], keys["d"] )

    # encryption with salt k
    def encrypt_int( self, m, e, n, k ):
        salt = rand( 2**(k-1), 2**k-1)
        m = m << k
        m += salt
        if m >= n:
            raise RuntimeError("Salted message too large")
        return expmod( m, e, n )

    # decryption with salt k
    def decrypt_int( self, c, d, n, k ):
        m = expmod( c, d, n )
        return m >> k

    def encrypt( self, m: bytes, e, n, k ):
        return self.encrypt_int( int.from_bytes( m, 'big' ), e, n, k )

    def decrypt( self, c: int, l: int, d, n, k ):
        return self.decrypt_int( c, d, n, k ).to_bytes( l, 'big' )
