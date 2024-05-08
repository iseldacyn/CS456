from rsa import RSA
from aes import AES
from data import Data
from color import *
from pickle import dumps, loads
import socket, threading

LOGIN = 0
LISTUSERS = 1
LOGOUT = 2
SENDMESSAGE = 3
SERVER = 4

BUF_LEN = 2048
SALT_LEN = 8


# client object that runs on user device
class Client:
    def __init__( self, username, hostname, port, rsa: RSA, aes_l: int ):
        self.username = username
        self.hostname = hostname
        self.port = port
        self.rsa = rsa
        self.aes_l = aes_l
        self.disconnect = False
        self.aes = None
        self.data_to_server = None
        self.data_from_server = None
        self.channel = None

    def start(self):
        # connect to host server
        self.channel = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.channel.connect( (self.hostname, self.port) )

        # exchange RSA keys and get aes key
        pic( "Connecting to server...", BLUE )
        self.init_keys()

        # create listener for messages
        pic( "Connection Established!", GREEN )
        server_listener = ServerListener( self )
        thread = threading.Thread( target=server_listener.start )
        thread.start()

        # add user to list of users
        self.data_to_server = Data( self.username, '', LOGIN )
        self.send_data()

        # read and send data
        try:
            while not self.disconnect:
                self.read_data()
                self.send_data()
        except KeyboardInterrupt:
            # send logout message and close socket
            self.disconnect = True
            self.data_to_send = Data( self.username, self.username + "has disconnected", LOGOUT )
            self.send_data()

        # shutdown and close socket
        pic( "Connection Terminated", RED )
        self.channel.shutdown( socket.SHUT_RDWR )
        thread.join()

    # read user input data
    def read_data(self):
        user_input = input()

        # quit from session
        if user_input == "QUIT":
            self.disconnect = True
            self.data_to_server = Data( self.username, self.username + " has disconnected", LOGOUT )

        # list current connected users
        elif user_input == "LISTUSERS":
            self.data_to_server = Data( self.username, '', LISTUSERS )

        # send a message
        else:
            self.data_to_server = Data( self.username, user_input, SENDMESSAGE )

    # update to encrypt
    # send data to server
    def send_data(self):
        self.data_to_server = self.aes.encrypt( dumps(self.data_to_server) )
        self.channel.send( self.data_to_server )

    # update to decrypt
    # get data from server
    def get_data(self):
        data = self.channel.recv(BUF_LEN)
        if data != b'':
            self.data_from_server = loads( self.aes.decrypt(data) )

    # print messages seen by listener
    def print_data(self):
        if self.data_from_server.type_ == SERVER:
            pic( self.data_from_server.message, YELLOW )
        if self.data_from_server.type_ == LISTUSERS:
            pic( "User List:\n" + self.data_from_server.message, YELLOW )
        elif self.data_from_server.type_ == LOGOUT:
            pic( self.data_from_server.message, RED )
        else:
            if self.data_from_server.username is None:
                return
            pic( "User: " + CYAN + self.data_from_server.username, YELLOW )
            pic( "Date: " + CYAN + self.data_from_server.date, YELLOW )
            pic( self.data_from_server.message, CYAN )

    def init_keys(self):
        # get server public keys
        n, e = loads( self.channel.recv(BUF_LEN) ).message
        # encrypt pub keys and send
        encr_n = self.rsa.encrypt_int( self.rsa.n, e, n, SALT_LEN )
        encr_e = self.rsa.encrypt_int( self.rsa.e, e, n, SALT_LEN )
        self.data_to_server = Data( None, (encr_n, encr_e, self.aes_l), None )
        self.channel.send( dumps(self.data_to_server) )
        # decrypt aes key from server
        key, l_k, seed, l_s = loads( self.channel.recv(BUF_LEN) ).message
        key = self.rsa.decrypt( key, l_k, self.rsa.d, self.rsa.n, SALT_LEN )
        seed = self.rsa.decrypt( seed, l_s, self.rsa.d, self.rsa.n, SALT_LEN )
        self.aes = AES( key, seed )
                
# listener class for clients to get data from server
class ServerListener(threading.Thread):
    def __init__( self, client ):
        self.client = client

    # get data and print it to terminal of the client
    def start(self):
        while not self.client.disconnect:
            self.client.get_data()
            if self.client.disconnect:
                return
            self.client.print_data()
