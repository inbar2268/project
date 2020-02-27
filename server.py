import socket
from threading import Thread

class HandleClient(Thread):  
    clients =[]  #class variable
    symbols = [["o",True], ["x",False]]
    def __init__(self, client_socket):
        Thread.__init__(self)
        #print(self.getName(), client_socket)
        self.client_socket = client_socket
        HandleClient.clients.append(client_socket)
        s = HandleClient.symbols[0][0]
        t = HandleClient.symbols[0][1]
        HandleClient.symbols.pop(0)
        data = "symbol," + s + "," +str(t)
        self.client_socket.send(data.encode('ascii'))

    
    def run(self):
        while(1):
            client_info = self.client_socket.recv(1024)
            HandleClient.broadcast(client_info)
            client_info_str = client_info.decode('ascii')
            
            if client_info_str == "":
                self.client_socket.close()
                print ("client close the socket")
                HandleClient.clients.remove(self.client_socket)
                break
            print ("server got: " + client_info_str)
            #data = client_info_str[::-1]
            data = client_info_str

            self.client_socket.send(data.encode('ascii'))

    @classmethod
    def broadcast(cls, msg):  
        for sock in cls.clients:
            sock.send( msg)


class Server():
    def __init__(self, port):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0',5578))
        self.server_socket.listen(5)

    def go(self):     
        while(1):
            (client_socket, client_address) = self.server_socket.accept()
            a = HandleClient(client_socket)
            a.start()


           

a = Server(9987)
a.go()