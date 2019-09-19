import socket
import threading
import sys
import time
from random import randint

class Server:
    connections = []
    lenConnections = len(connections)
    peers = []
    lastMessages = []
    encoding = "iso-8859-1"

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
                self.peers.append(a[0])
                print(str(a[0]) + " : " + str(a[1]), "connected")
                self.sendPeers()


    def handler(self,c,a):
        while True:
            data = c.recv(1024)

            if len(self.lastMessages) < 10 and data != b'\x12':
                self.lastMessages.append(data)
            else:
                self.lastMessages.append(data)
                del(self.lastMessages[0])

            if data[0:1] == b'\x12':
                if self.lastMessages != []:
                    c.send(bytes("Recently sent messages: \n", self.encoding))
                    for message in self.lastMessages:
                        c.send(message + bytes("\n", self.encoding))

            for connection in self.connections:
                connection.send(data)

            if not data:
                print(str(a[0]) + " : " + str(a[1]), "disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))




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
