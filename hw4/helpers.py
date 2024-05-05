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

class Point:
    def __init__( self, x, y ):
        self.x = x
        self.y = y
    def __str__( self ):
        return str(self.x) + ', ' + str(self.y)

# P = (x1,y1); Q = (x2,y2); p, a from curve
def add_points( P, Q, a, p ):
    if P == 'i':
        return Q
    elif Q == 'i':
        return P
    elif P.x == Q.x:
        if P.y == Q.y:
            # (3x1^2+a) / (2y1)
            _, i = xgcd( p, (2*P.y)%p )
            while i < 0:
                i += p
            m = (3*P.x*P.x + a) % p
            m = (m*i) % p
            c = (P.y - m*P.x) % p

            x3 = (m*m - 2*P.x) % p
            y3 = (m*x3 + c) % p
            return Point( x3, (-1*y3)%p )
        elif P.y == -Q.y:
            return 'i'
    else:
        # (x2-x1) / (y2-y1)
        if P.x > Q.x:
            _, i = xgcd( p, (P.x-Q.x)%p )
            while i < 0:
                i += p
            m = ((P.y-Q.y)*i) % p
        else:
            _, i = xgcd( p, (Q.x-P.x)%p )
            while i < 0:
                i += p
            m = ((Q.y-P.y)*i) % p
        c = (P.y - m*P.x) % p

        x3 = (m*m - (P.x+Q.x)) % p
        y3 = (m*x3 + c) % p
        return Point( x3, (-1*y3)%p )
