from helpers import *

if __name__ == '__main__':
    # read in cipher
    cipher = int( open( 'a2.cipher', 'r' ).readlines()[0] )

    # read public keys
    keys = open( 'a2.pubkeys', 'r' ).readlines()
    n = int( keys[0].replace( '\n', '' ) )
    e = int( keys[1] )
    
    # read hint
    phi = int( open( 'a2.hint', 'r' ).readlines()[0] )

    _, d = xgcd( phi, e )
    while d < 0:
        d += phi
    decipher = rsa_decrypt( cipher, d, n )

    # decipher to mono cipher
    monotext = open( 'a2.mono', 'w' )
    freq = {}
    while decipher:
        curr_char = decipher & 0xFF
        curr_char = chr(curr_char)
        if curr_char not in freq:
            freq.update( {curr_char:1} )
        else:
            freq[curr_char] += 1
        decipher >>= 8
        monotext.write( curr_char )
        
    # start to do freq analysis
    monotext.close()
    cipher2 = open( 'a2.mono', 'r' ).readlines()
    max_freq = max( freq, key = freq.get )
    freq[max_freq] -= freq[max_freq]
    max_freq2 = max( freq, key = freq.get )

    plaintext = open( 'a2.plaintext', 'w' )
    for line in range(len(cipher2)):
        # e is max freq, then t
        cipher2[line] = cipher2[line].replace( max_freq, 'E' )
        cipher2[line] = cipher2[line].replace( max_freq2, 'T' )
        cipher2[line] = cipher2[line].replace( '5', 'A' )
        # see some aa -> oo
        cipher2[line] = cipher2[line].replace( 'a', 'O' )
        # ;4 -> th
        cipher2[line] = cipher2[line].replace( '4', 'H' )
        # )HOT -> SHOOT
        cipher2[line] = cipher2[line].replace( ')', 'S' )
        # *O(THEAST -> NORTHEAST
        cipher2[line] = cipher2[line].replace( '*', 'N' )
        cipher2[line] = cipher2[line].replace( '(', 'R' )
        # ANb -> AND
        cipher2[line] = cipher2[line].replace( 'b', 'D' )
        # 6N -> IN
        cipher2[line] = cipher2[line].replace( '6', 'I' )
        # DEcI0 -> DEVIL
        cipher2[line] = cipher2[line].replace( 'c', 'V' )
        cipher2[line] = cipher2[line].replace( '0', 'L' )
        # 3OOD -> GOOD
        cipher2[line] = cipher2[line].replace( '3', 'G' )
        # 2ISHO7S -> BISHOPS
        cipher2[line] = cipher2[line].replace( '2', 'B' )
        cipher2[line] = cipher2[line].replace( '7', 'P' )
        # 9IN?TES -> MINUTES
        cipher2[line] = cipher2[line].replace( '9', 'M' )
        cipher2[line] = cipher2[line].replace( '?', 'U' )
        # 1I1T: 1EET -> FIFTY FEET
        cipher2[line] = cipher2[line].replace( '1', 'F' )
        cipher2[line] = cipher2[line].replace( ':', 'Y' )
        # BRAN-H -> BRANCH
        cipher2[line] = cipher2[line].replace( '-', 'C' )
        plaintext.write( cipher2[line] )
