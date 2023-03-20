from clientSSLRemoteCommands import *
from clientSSLFunRC import *
from clientSSL2 import *
from clientSSLgeneral import *
import ssl
from socket import *
import socket
#openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt

IP = "localhost"
PORT = 12000
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"

server_sni_hostname = 'ComputerNetworksProject.(BSdC)'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

#Controllo certificato di connessione
def controlConnection():

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    return context


#Collegamento al server
def clientConnections():
    try:
        context = controlConnection()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
        client.connect(ADDR)
        return client
    except:
        #traceback.print_exc()
        return "errore"
    #print("SSL established. Peer: {}".format(client.getpeercert()))


# OK creazione connessione
def clientConnection():
    IP = "localhost"
    PORT = 12000
    ADDR = (IP, PORT)
    SIZE = 4096
    FORMAT = "utf-8"
    try:
        client = socket.socket(AF_INET, SOCK_STREAM)
        client.connect(ADDR)
        return client
    except:
        #traceback.print_exc()
        return "errore"

