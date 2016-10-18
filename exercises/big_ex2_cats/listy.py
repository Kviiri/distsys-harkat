import socket
import threading

sock = socket.socket()

with open("port_number", "r") as f:
    port = int(f.readline)

sock.bind(('localhost', port))

sock.listen(5)
with open("cmesg", "a") as log:
    fileLock = Lock()
    catSock = a.accept()[0].makefile()
    Thread(target = receive, args = (catSock, log))


def receive(cat, log):
    while True:
        msg = cat.readline
        if validate(msg):
            fileLock.acquire()
            log.write(msg + "\n")
            fileLock.release()

