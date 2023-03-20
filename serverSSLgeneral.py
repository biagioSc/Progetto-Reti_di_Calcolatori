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
from cryptography.fernet import Fernet

# OK funzione di pulizia schermo per unix e windows
def clearScreen():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


def regexcheck_find(comando):
    windows_regex=r'^find \.[a-z]{1,4} (\.(\\[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\\[a-zA-Z0-9, ,\_,\-]+)+)'
    unix_regex='^find \.[a-z]{1,4} (\.(\/[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\/[a-zA-Z0-9, ,\_,\-]+)+)'
    resultWindows = 'null'
    resultUnix = 'null'

    resultWindows = re.match(windows_regex,comando)
    resultUnix = re.match(unix_regex,comando)

    if resultWindows or resultUnix:
        return True
    else:
        return False


# OK gestisce il ctrl-C per l'uscita
def signalHandler(signum, frame):
    msg = "Uscita effettuata con successo"
    print(":", msg, end="", flush=True)
    exit(1)


def regexcheck_ls(comando):
    windows_regex = '^ls ([a-zA-Z0-9, ,\-,\_]+)|^ls (\\[a-zA-Z0-9, ,\-,\_]+)+|^ls (\.(\\[a-zA-Z0-9, ,\-,\_]+)+)|^ls \.\.|^ls \.|^ls'
    unix_regex = '^ls ([a-zA-Z0-9, ,\-,\_]+)|^ls (\/[a-zA-Z0-9, ,\-,\_]+)+|^ls (\.(\/[a-zA-Z0-9, ,\-,\_]+)+)|^ls \.\.|^ls \.|^ls'

    if re.match(unix_regex,comando) or re.match(windows_regex,comando):
        return True
    else:
        return False


def regexcheck_download(comando):

    windows_regex_tip1 = r'^download "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^download \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'
    windows_regex_tip2 = r'^download "[\s\S]+\.[a-z]{1,4}" nel percorso: C:(\\[^\/]+)+'
    unix_regex_tip2 = '^download \"[\s\S]+\.[a-z]{1,4}\" nel percorso: (\/[^\/]+)+'

    result1 = 'null'
    result2 = 'null'

    if re.match(windows_regex_tip1,comando):
        return "windowstip1"
    elif re.match(windows_regex_tip2,comando):
        return "windowstip2"
    elif re.match(unix_regex_tip1,comando):
        return "unixtip1"
    elif re.match(unix_regex_tip2,comando):
        return "unixtip2"
    else:
        return "not matched"


def regexcheck_openZip(comando):

    windows_regex_tip1 = r'^open "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^open \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'

    if re.match(windows_regex_tip1,comando):
        return "windowstip1"
    elif re.match(unix_regex_tip1,comando):
        return "unixtip1"
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


def regexcheck_print(comando):

    windows_regex_tip1 = r'^printFile "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^printFile \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'

    if re.match(windows_regex_tip1,comando):
        return "windowstip1"
    elif re.match(unix_regex_tip1,comando):
        return "unixtip1"
    else:
        return "not matched"