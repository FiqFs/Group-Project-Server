import socket
import os
import threading
import hashlib


ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '192.168.0.193'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
HashTable = {}

def threaded_client(connection):
    connection.send(str.encode('ENTER USERNAME : '))
    name = connection.recv(2048)
    connection.send(str.encode('ENTER PASSWORD : '))
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    password=hashlib.sha512(str.encode(password)).hexdigest()

    if name not in HashTable:
        HashTable[name]=password
        connection.send(str.encode('Registeration Successful')) 
        print('Registered : ',name)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        
    else:
        if(HashTable[name] == password):
            connection.send(str.encode('Login Successful')) 
            print('Connected : ',name)
        else:
            connection.send(str.encode('Login Failed'))
            print('Connection denied : ',name)
    while True:
        break
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()
