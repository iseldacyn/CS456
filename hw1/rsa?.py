from helpers import *

if __name__ == '__main__':
    # get keys from file
    keys = open( 'a1.privkeys', 'r' ).readlines()
    n = int( keys[0].replace( '\n', '' ) )
    e = int( keys[1].replace( '\n', '' ) )
    d = int( keys[2].replace( '\n', '' ) )

    # open file for decrypting and decrypt
    c = open( 'a1.encrypted', 'r' ).readlines()
    plaintext = open( 'a1.decrypted', 'w' )
    for line in c:
        curr_char = int( line.replace('\n','') )
        plaintext.write( chr(rsa_decrypt( curr_char,  d, n )) )
