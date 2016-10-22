import socket
import threading

def receive(cat, log):
    msg = cat.readline()
    fileLock.acquire()
    log.write(msg + "\n")
    log.flush()
    fileLock.release()


sock = socket.socket()

with open("port_number", "r") as f:
    port = int(f.readline())

sock.bind(('0.0.0.0', port))

sock.listen(5)
with open("cmsg", "a") as log:
    fileLock = threading.Lock()
    while True:
        catSock = sock.accept()[0].makefile()
        threading.Thread(target = receive, args = (catSock, log)).start()




