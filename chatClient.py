import socket
import threading
import sys
import time
import os
from random import randint
from datetime import datetime

class Client:
    encoding = "iso-8859-1"
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%H:%M")
    username = ""

    def delete_last_lines(self, n):
        for _ in range(n):
            sys.stdout.write('\x1b[1A') # Back to previous line
            sys.stdout.write('\x1b[2K') # Delete line

    def sendMsg(self, username, sock):
        while True:
            try:
                sock.send(bytes(self.timeStampStr + ": " + username + ": " + input(""), self.encoding))
                self.delete_last_lines(1)
            except BrokenPipeError:
                sys.exit(0)

    def __init__(self, address):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 32555))

        print("Successfully connected!")
        username = (input("Choose a username: ")).upper()
        sock.send(b'\x12')

        iThread = threading.Thread(target=self.sendMsg, args=(username, sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(str(data,self.encoding))


os.system('cls' if os.name == 'nt' else 'clear')
while True:
    try:
        print("Trying to connect...")
        time.sleep(randint(1,5))
        try:
            client = Client("217.160.61.229")
        except KeyboardInterrupt:
            print("\n Successfully exitted...")
            sys.exit(0)
        except:
            pass

    except KeyboardInterrupt:
        print("\n Successfully exitted...")
        sys.exit(0)
