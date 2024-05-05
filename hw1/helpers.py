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
    return x2, y2

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

# m^e (mod n)
def rsa_encrypt( m, e, n ):
    return expmod( m, e, n )

# c^d (mod n)
def rsa_decrypt( c, d, n ):
    return expmod( c, d, n )
