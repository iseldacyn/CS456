from helpers import *

if __name__ == "__main__":
    # read cipher text
    ciphertext = open( 'a3.cipher', 'r' ).readlines()
    cipher = []
    for line in ciphertext:
        line = line.split(',')
        cipher.append( [int(line[0]), int(line[1])] )

    # read public keys + secret a
    keys = open( 'a3.pubkeys', 'r' ).readlines()
    p = int( keys[0].replace(' ','').split('=')[1] )
    g = int( keys[1].replace(' ','').split('=')[1] )
    b = int( keys[2].replace(' ','').split('=')[1] )
    a = int( open( 'a4.plaintext', 'r' ).readlines()[0].replace(' ','').split('=')[1] )

    plaintext = open( 'a3.plaintext', 'w' )
    for line in cipher:
        m = elgamal_decrypt( line[1], line[0], a, p )
        plaintext.write( chr(m) )
