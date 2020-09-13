from socket import *

HOST = '127.0.0.1'  # or 'localhost'
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:

    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print(data.decode("utf-8"))

tcpCliSock.close()
