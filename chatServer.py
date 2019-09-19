import socket
import threading
import sys
import time
import os
from random import randint
from datetime import datetime

class Server:
    connections = []
    lenConnections = len(connections)
    lastMessages = []
    encoding = "iso-8859-1"
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d/%m/%y-%H:%M")

    def __init__(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', 32555))
            sock.listen(1)
            print("Server running...")

            while True:
                c,a = sock.accept()
                cThread = threading.Thread(target = self.handler, args = (c, a))
                cThread.daemon = True
                cThread.start()
                self.connections.append(c)
                #print(str(a[0]) + " : " + str(a[1]), "connected")
                print("%s : %s : %s connected" % (self.timeStampStr,str(a[0]),str(a[1])))


    def handler(self,c,a):
        while True:
            data = c.recv(1024)

            if len(self.lastMessages) < 10 and data != b'\x12':
                self.lastMessages.append(data)
            elif data != b'\x12':
                self.lastMessages.append(data)
                del(self.lastMessages[0])

            try:
                if data == b'\x12':
                    if self.lastMessages != []:
                        c.send(bytes("Recently sent messages: \n", self.encoding))
                        for message in self.lastMessages:
                            c.send(message + bytes("\n", self.encoding))

                for connection in self.connections:
                    connection.send(data)
            except BrokenPipeError:
                pass

            if not data:
                print("%s : %s : %s disconnected" % (self.timeStampStr,str(a[0]),str(a[1])))
                self.connections.remove(c)
                c.close()
                break


os.system('cls' if os.name == 'nt' else 'clear')
while True:
    try:
        print("Trying to start server...")
        time.sleep(randint(1,5))
        try:
            server = Server()
        except KeyboardInterrupt:
            print("\n Successfully exitted...")
            sys.exit(0)
        except:
            print("Couldn't start the server...")

    except KeyboardInterrupt:
        print("\n Successfully exitted...")
        sys.exit(0)
