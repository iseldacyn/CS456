from classes_server import *
from rsa import RSA
import re

if __name__ == '__main__':
    # check for valid port number
    while True:
        port = iic( "Port (default 7000): ", BLUE )
        not_valid = False
        if not port:
            port = "7000"
            break
        elif not re.match( r"^([0-9]*)$", port ):
            pic( "Port must only be integers!", RED )
        elif int(port) < 1024 or int(port) > 65535:
            pic( "Port must be greater than 1024 and less than 65535", RED )
        else:
            break

    # generate RSA keys
    while True:
        k = iic( "Choose RSA key bit length (2048, 4096): ", BLUE )
        if k not in ["2048", "4096"]:
            pic( "Bit length must be either 2048 or 4096!", RED )
        else:
            break

    k = int(k)
    pic( "Generating RSA keys...", BLUE )
    rsa = RSA.generate(k)

    server = Server( int(port), rsa )
    server.start()
