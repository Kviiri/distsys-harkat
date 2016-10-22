import socket
import threading

sock = socket.socket()

with open("port_number", "r") as f:
    port = int(f.readline())

sock.bind(('localhost', port))

sock.listen(5)
with open("cmsg", "a") as log:
    fileLock = threading.Lock()
    while True:
        catSock = sock.accept()[0].makefile()
        Thread(target = receive, args = (catSock, log))


def receive(cat, log):
    msg = cat.readline()
    if validate(msg):
        fileLock.acquire()
        log.write(msg + "\n")
        fileLock.release()

