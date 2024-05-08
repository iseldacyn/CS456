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

BUF_LEN = 2048
SALT_LEN = 8

# for synchronized methods
# "java locks in python" from https://theorangeduck.com/page/synchronized-python
def synchronized_with_attr(lock_name):
    def decorator(method):
        def new_method( self, *args, **kws ):
            lock = getattr( self, lock_name )
            with lock:
                return method( self, *args, **kws )
        return new_method
    return decorator

# server object that runs in the background
class Server:
    def __init__( self, port: int, rsa: RSA ):
        self.port = port
        self.rsa = rsa
        self.disconnect = False
        self.clientIO_list = []
        self.user_list = []
        self.lock = threading.RLock()

    def start(self):
        # create a new socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        # avoid "Address already in use" error when clients join
        sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        sock.bind( ('', self.port) )

        while not self.disconnect:
            sock.listen()
            pic( "Searching for clients...", BLUE )

            # create new socket for client and append to client list
            new_client_sock, _ = sock.accept()
            pic( "Client found!", GREEN )
            new_client = ClientIO( self, new_client_sock )

            # add client to list and create new thread for them
            self.clientIO_list.append( new_client )
            thread = threading.Thread( target=new_client.start, daemon=True )
            thread.start()

        sock.shutdown( socket.SHUT_RDWR )

    # send message to all users
    @synchronized_with_attr("lock")
    def broadcast( self, data_to_broadcast ):
        if not self.clientIO_list:
            return
        for client in self.clientIO_list:
            if client.data_from_client.type_ == LOGOUT:
                continue
            client.data_to_client = data_to_broadcast
            client.send_data()

    # send message to only one user
    @synchronized_with_attr("lock")
    def broadcast_to( self, data_to_broadcast ):
        for client in self.clientIO_list:
            if client.data_from_client == data_to_broadcast:
                data_to_broadcast.message = self.get_users()
                client.data_to_client = data_to_broadcast
                client.send_data()

    # remove a user from list
    @synchronized_with_attr("lock")
    def remove( self, client_to_remove, username ):
        self.user_list.remove( client_to_remove.username )
        self.clientIO_list.remove( client_to_remove )
        
    # add a user to list
    @synchronized_with_attr("lock")
    def add( self, username ):
        self.user_list.append( username )

    # return string of all users
    def get_users(self):
        users = ''
        for user in self.user_list:
            users += user + '\n'
        return "User List:\n" + users

# class for individual client threads running on server
class ClientIO( threading.Thread ):
    def __init__( self, server: Server, sock: socket ):
        self.server = server
        self.client_socket = sock
        self.disconnect = False
        self.data_to_client = None
        self.data_from_client = None
        self.aes = None

    def start(self):
        # exchange RSA keys and generate shared AES key
        self.init_keys()

        while not self.disconnect:
            self.get_data()

            # someone joins chat
            if self.data_from_client.type_ == LOGIN:
                self.server.broadcast_to( self.data_from_client )
                continue

            # list active users
            elif self.data_from_client.type_ == LISTUSERS:
                self.server.broadcast_to( self.data_from_client )

            # send message
            else:
                self.server.broadcast( self.data_from_client )
        
        # shutdown and close sockets
        self.server.remove( self, data_from_client.username )
        self.client_socket.shutdown( socket.SHUT_RDWR )

    # get data from stream
    def get_data(self):
        data = self.client_socket.recv(BUF_LEN)
        if data != b'':
            self.data_from_client = loads( self.aes.decrpyt(data) )

        # logout of server
        if self.data_from_client == LOGOUT:
            self.disconnect = True

        # add new user
        elif self.data_from_client.type_ == LOGIN:
            self.server.add( self.data_from_client.username )

    # send data to stream
    def send_data(self):
        self.data_to_client = self.aes.encrypt( dumps(self.data_to_client) )
        self.client_socket.send( self.data_to_client )

    def init_keys(self):
        # send public key
        self.data_to_client = Data( None, (self.server.rsa.n, self.server.rsa.e), None )
        self.client_socket.send( dumps(self.data_to_client) )
        # get encrypted public key and decrypt
        n, e, aes_l = loads( self.client_socket.recv(BUF_LEN) ).message
        n = self.server.rsa.decrypt_int( n, self.server.rsa.d, self.server.rsa.n, SALT_LEN )
        e = self.server.rsa.decrypt_int( e, self.server.rsa.d, self.server.rsa.n, SALT_LEN )
        # make aes key, encrypt and send
        self.aes = AES.generate( aes_l )
        encr_key = self.server.rsa.encrypt( self.aes.key, e, n, SALT_LEN )
        encr_seed = self.server.rsa.encrypt( self.aes.seed, e, n, SALT_LEN )
        self.data_to_client = Data( None, (encr_key, len(self.aes.key), encr_seed, len(self.aes.seed)), None )
        self.client_socket.send( dumps( self.data_do_client ) )
