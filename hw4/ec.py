from helpers import *

if __name__ == "__main__":
    # read in cipher
    cipher_text = open( 'a4.cipher', 'r' ).readlines()
    cipher = []
    for line in cipher_text:
        line = line.split(' ')
        cipher.append( [Point(int(line[0]), int(line[1])), Point(int(line[2]), int(line[3]))] )

    # read in keys
    keys = open( 'a4.keys', 'r' ).readlines()
    p = int( keys[0].replace(' ','').split('=')[1] )
    A = int( keys[1].replace(' ','').split('=')[1] )
    B = int( keys[2].replace(' ','').split('=')[1] )
    G = keys[3].replace(' ','').replace('[','').replace(']','').split('=')[1].split(',')
    G = Point( int(G[0]), int(G[1]) )
    P = keys[4].replace(' ','').replace('[','').replace(']','').split('=')[1].split(',')
    P = Point( int(P[0]), int(P[1]) )
    N = int( keys[6].replace(' ','').split('=')[1] )

    # decipher plaintext
    plaintext = open( 'a4.plaintext', 'w' )
    for point in cipher:
        c = point[0]
        halfmask = point[1]
        
        fullmask = add_points( halfmask, halfmask, A, p )
        fullmask = add_points( fullmask, halfmask, A, p )
        fullmask.y = (-1*fullmask.y) % p

        plaintext.write( chr(add_points(c, fullmask, A, p).x) )
