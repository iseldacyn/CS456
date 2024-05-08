from classes_client import *
from color import *
from rsa import RSA
import re

if __name__ == '__main__':
    # check for valid username
    not_valid = True
    while not_valid:
        username = iic( "Username: ", BLUE )
        not_valid = False
        if not username:
            pic( "Username must not be empty!", RED )
            not_valid = True
        for char in username:
            if not re.match( r"^([a-zA-Z0-9\_]*)$", char ):
                pic( "Username must not contain " + char, RED )
                not_valid = True


    # check for valid hostname
    not_valid = True
    while not_valid:
        hostname = iic( "Hostname (default 127.0.0.1): ", BLUE )
        not_valid = False
        if not hostname or hostname == 'localhost':
            hostname = '127.0.0.1'
        elif len(hostname.split('.')) != 4:
            not_valid = True
            pic( "Hostname must be of the form X.X.X.X or localhost", RED )

    # check for valid port number
    not_valid = True
    while not_valid:
        port = iic( "Port (default 7000): ", BLUE )
        not_valid = False
        if not port:
            port = "7000"
        if not re.match( r"^([0-9]*)$", port ):
            pic( "Port must only be integers!", RED )
            not_valid = True
        elif int(port) < 1024 or int(port) > 65535:
            pic( "Port must be greater than 1024 and less than 65535", RED )
            not_valid = True

    # generate RSA keys
    not_valid = True
    while not_valid:
        k = iic( "Choose RSA key bit length (1024, 2048, 4096): ", BLUE )
        not_valid = False
        if k not in ["1024", "2048", "4096"]:
            pic( "Bit length must be one of 1024, 2048, or 4096!", RED )
            not_valid = True
    k = int(k)
    pic( "Generating RSA keys...", BLUE )
    rsa = RSA.generate(k)

    # generate AES block size
    while True:
        k = iic( "Choose AES key size (128, 192, 256): ", BLUE )
        if k not in [ "128", "192", "256" ]:
            pic( "AES key size must be one of 128, 192, or 256!", RED )
        else:
            break
    aes_l = int(k)

    client = Client( username, hostname, int(port), rsa, aes_l )
    client.start()
