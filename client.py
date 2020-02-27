import sys
from socket import *
from threading import Thread
from wx.lib.pubsub import pub
from queue import Queue
from time import sleep

conn_q = Queue()
#gui_q  = Queue()

conn_q = Queue()
#gui_q  = Queue()

def client_recv(my_socket):
    while True:
        data = my_socket.recv(1024)
        if data=="":
            print("server close this socket")
            my_socket.close()
            break #get out from thread
        data = data.decode('latin-1')
        print ("client_recv:" + data )
        #print("4444",current_thread().name)
        #gui_q.put(data)
        pub.sendMessage("update", msg="server response " +data)

def client_send():
    print("start client")
    my_socket = socket()
    my_socket.connect(("127.0.0.1",5578))
    #my_socket.connect(("10.0.0.31",8820))

    recvThread = Thread(target=client_recv, args=(my_socket,))
    recvThread.start()

    while True:
        if conn_q.empty() == False:
            data = conn_q.get()
            print ("client_send:" + data )
            #print("3333",current_thread().name)
            my_socket.sendall(data.encode('latin-1'))
        sleep(0.05) #sleep a little before check the queue again

