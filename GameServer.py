import socket
import sys

def manageClientConnections():
    # method to manage client connetions
    # multi threading begins here


def initialize():
    # method to start server and set up connection for client to connect to
    
    # set up host to accept clients with any host name, and arbitary non
    # privledged port
    HOST = ''
    PORT = 21313

    # Create socket with ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # attempt to bind socket to host and port
    try:
        sock.bind(HOST, PORT)
    except socket.error as msg:
        print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # start listening for a connection, parameter is max number of queued
    # connections
    sock.listen(10)

    #infinite loop to wait on client connections
    while True:
        # clientSock = new socket object to allow data to be exchanged
        # address is address of cliSock on client's end of communication
        clientSock, address = sock.accept()          
        
        if (clientSock!=''):
            print 'Server: Connection established to client %s', address


if __name__ == '__main__':
    initialize()      
