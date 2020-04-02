import socket
import threading
import sys

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self, port):
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(1)
        print("Server running on port " + str(port))
    def handler(self,c,a):
        while True:
            data = c.recv(1024)
            res = self.cmdHandler(data)
            for connection in self.connections:
                connection.send(bytes(res,'utf-8'))
            if not data:
                break
    def run(self):
        while True:
            c,a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(self.connections)
    def cmdHandler(cmd):
        if "myip" in cmd:
            return self.connections


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""),'utf-8'))
    def __init__(self, address, port):
        self.sock.connect((address, port))

        inputThread = threading.Thread(target=self.sendMsg)
        inputThread.daemon = True
        inputThread.start()

        while True:
            data = self.sock.recv(1024)
            #check if client has disconnected
            if not data:
                break
            print(data)
def helpCmds():
    print("myip - display IP of this process")
    print("myport - display port")
    print("connect <destination> <port no> - connect to server")
    print("list - list clients")
    print("terminate  <connection  id.>  - This  command  will  terminate  the  connection  listed  under  the  specifiednumber  when  LIST  is  used  to  display  all  connections.")
    print("send <connection id.> <message> (For example, send 3 Oh! This project is a piece of cake). This willsend the message to the host on the connection that is designated by the number ")
    print("exit - close all connections")

if(len(sys.argv) > 1):
    server = Server(int(sys.argv[1]))
    server.run()
else:
    print("Running as client")
    ip = input("Enter ip ")
    port = input("Enter port ")
    client = Client(ip, int(port))

