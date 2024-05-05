from helpers import *

if __name__ == '__main__':
    # read cipher text from file
    cipher_file = open( 'a1.cipher', 'r' )
    c = cipher_file.readlines()
    for line in range(len(c)):
        c[line]= int( c[line].replace( '\n', '' ) )

    # read public keys n, e from file
    pubkeys_file = open( 'a1.pubkeys', 'r' )
    pubkeys = pubkeys_file.readlines()
    n = int( pubkeys[0].replace( '\n', '' ) )
    e = int( pubkeys[1].replace( '\n', '' ) )

    ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .\n'
    encoded_char = {}

    for char in ascii:
        encoded_char.update( {rsa_encrypt( ord(char), e, n ): char} )

    plaintext_file = open( 'a1.plaintext', 'w' )

    for char in c:
        if char in encoded_char:
            plaintext_file.write( encoded_char[char] )
