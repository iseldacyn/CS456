from datetime import datetime

# class for sending data between clients
class Data:
    def __init__( self, username, message, type_  ):
        self.username = username
        self.message = message
        self.type_ = type_
        self.date = datetime.now().strftime( "%m/%d/%y %H:%M:%S" )

