import socket
import threading
import sys
import time
from random import randint
from datetime import datetime

class Client:
    encoding = "iso-8859-1"
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%H:%M")

    def delete_last_lines(self, n):
        for _ in range(n):
            sys.stdout.write('\x1b[1A') # Back to previous line
            sys.stdout.write('\x1b[2K') # Delete line

    def sendMsg(self, username, sock):
        while True:
            sock.send(bytes(self.timeStampStr + ": " + username + ": " + input(""), self.encoding))
            self.delete_last_lines(1)


    def __init__(self, address):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 32555))

        print("Successfully connected!")
        username = (input("Choose a username: ")).upper()
        iThread = threading.Thread(target=self.sendMsg, args=(username, sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data,self.encoding))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, self.encoding).split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']

while True:
    try:
        print("Trying to connect...")
        time.sleep(randint(1,5))
        for peer in p2p.peers:
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
