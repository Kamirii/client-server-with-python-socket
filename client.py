import socket
import threading
import sys
import time


client_host = "127.0.0.1"
client_process_port = int(input('Enter client port: '))

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((client_host, client_process_port))


# recv connected message
dataServer = clientSocket.recv(2024).decode()
print(dataServer)


# ask input username
dataServer = clientSocket.recv(2024).decode()
user = input(dataServer)
clientSocket.send(str.encode(user))


# ask input password
dataServer = clientSocket.recv(2024).decode()
password = input(dataServer)
clientSocket.send(str.encode(password))

# recv auth confirmation
dataServer = clientSocket.recv(2024).decode()
status = clientSocket.recv(2024).decode()
print(dataServer)
print(status)

# ask to write into file

if status == '202':
    while True:
        # send text data
        disconnected = "client disconnecting"
        dataServer = clientSocket.recv(2024).decode()
        data = input(dataServer)

        if data == 'sair':
            clientSocket.send(str.encode("client disconnecting"))
            print("disconnecting...")
            time.sleep(3)
            break
        else:
            clientSocket.send(str.encode(data))

clientSocket.close()
