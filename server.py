import socket
from threading import Thread
import sqlite3
import users1

class HandleClient(Thread):
    clients = []  # class variable
    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket
        HandleClient.clients.append(client_socket)
        self.u=users1.Users()

    def run(self):
        while (1):
            client_info = self.client_socket.recv(1024)
            HandleClient.broadcast(client_info)
            client_info_str = client_info.decode('ascii')

            if client_info_str == "":
                self.client_socket.close()
                print("client close the socket")
                HandleClient.clients.remove(self.client_socket)
                break
            msg = client_info_str.split(",")
            if msg[0]== "checkLogin":
                uAndP=(msg[1],msg[2])
                data= "checkLogin,"+str(self.check1(uAndP))

            if msg[0] == "checkSignUp":
                valid=self.check2(msg[1])
                data= "checkSignUp,"+str(valid)

            if msg[0] == "insertUser":
                self.u.insert_user(msg[1],msg[2])
                data="ok"

            print("server got: " + client_info_str)
            self.client_socket.send(data.encode('ascii'))

    @classmethod
    def broadcast(cls, msg):
        for sock in cls.clients:
            sock.send( msg)

    def check1(self, tup):
        conn = sqlite3.connect('users.db')
        cursor = conn.execute("SELECT * from USERS")
        exist = False
        for row in cursor:
            if (row == tup):
                exist = True
        return exist

    def check2(self, user):
        conn = sqlite3.connect('users.db')
        cursor = conn.execute("SELECT * from USERS")
        valid = True
        for row in cursor:
            if (row[0] == user):
                valid = False
        return valid

class Server():
    def __init__(self, port):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 5678))
        self.server_socket.listen(5)

    def go(self):
        while (1):
            (client_socket, client_address) = self.server_socket.accept()
            a = HandleClient(client_socket)
            a.start()


a = Server(5678)
a.go()