RED = '\u001b[31;1m'
GREEN = '\u001b[32m'
YELLOW = '\u001b[33;1m'
BLUE = '\u001b[34;1m'
CYAN = '\u001b[36;1m'
WHITE = '\u001b[37m'

# print in color
def pic( s, color ):
    print( color + s + WHITE )

# input in color
def iic( s, color ):
    return input( color + s + WHITE )

# string in color
def sic( s, color ):
    return color + s + WHITE
