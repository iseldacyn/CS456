from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CFB
from color import *
from math import ceil
import os
from random import getrandbits as rand

def generate_key( size ):
        return rand(size).to_bytes( ceil(size/8), 'big' )

def generate_seed():
    return os.urandom( AES.block_size // 8 )

class AES:
    def __init__( self, key, seed ):
        self.cipher = Cipher( AES(key), modes.CFB(seed) )
        self.key = key
        self.seed = seed

    def generate( size ):
        return AES( generate_key(size), generate_seed() )

    # symmetric encryption
    def encrypt( self, m ):
        encryptor = self.cipher.encryptor()
        return encryptor.update(m) + encryptor.finalize()

    # symmetric decryption
    def decrypt( self, c ):
        decryptor = self.cipher.decryptor()
        return decryptor.update(c) + decryptor.finalize()
