import socket
import sys
import threading
import time


server_host = '127.0.0.1'
server_process_port = int(input('Enter server port: '))


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serverSocket.bind((server_host, server_process_port))
    print('Server listening...')
except:
    print(str(sys.exc_info()))
    sys.exit()

print('Waiting for connections in:', server_process_port)
serverSocket.listen(3)


def create_file(msg, csocket, count):
    try:
        with open(f'msg{count}.txt', 'x') as f:
            f.write(msg)
            f.close()
    except:
        with open(f'msg{count}.txt', '+a') as f:
            f.write('\n' + msg)
            f.close()


def login_client(csocket, count):

    users = {'goethe': 'vienna', 'darwin': 'galapagos',
             'lovelace': 'algoritmo', 'albres': 'albres'}

    csocket.send(str.encode('From Server: ENTER USERNAME: '))
    user = csocket.recv(2048).decode()

    csocket.send(str.encode('From Server: ENTER PASSWORD: '))
    password = csocket.recv(2048).decode()

    user, password = user.strip(), password.strip()

    if user in users and password == users[user]:
        print(f"Client {count} authorized")
        csocket.send(str.encode(
            f'From Server: Current client {count}: authorized'))
        csocket.send(str.encode('202'))

        return True
    else:
        print(f"Client {count} not authorized")
        csocket.send(str.encode(
            f'From Server: Current client {count}: not authorized'))
        csocket.send(str.encode('401'))

        return False


def message_client(csocket, addr, count):
    csocket.send(str.encode(
        'From Server: Type your message or type "sair" \n '))
    data = csocket.recv(2048)
    msg = data.decode()
    create_file(msg, csocket, count)
    if msg == 'client disconnecting':
        return False
    else:
        return True


def init_thread_client(csocket, addr, count):
    print(f"New conection with client {count}: ", addr)
    csocket.send(str.encode('Connected with Server!'))

    if login_client(csocket, count):
        while message_client(csocket, addr, count):
            print("receive")
        print(f'client {count} disconnecting')


def start_program():
    serverSocket.listen(3)
    thread_count = 1

    while True:
        clientSocket, clientAddress = serverSocket.accept()
        newThread = threading.Thread(target=init_thread_client, args=(
            clientSocket, clientAddress, thread_count))
        newThread.start()
        thread_count += 1

    clientSocket.shutdown(socket.SHUT_RDWR)
    clientSocket.close()


start_program()
