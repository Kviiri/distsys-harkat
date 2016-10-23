import socket
import threading

def receive(cat, log):
    msg = cat.readline()
    fileLock.acquire()
    log.write(msg)
    log.flush()
    fileLock.release()
    #end after the mouse is a confirmed kill
    return msg.split()[0] == 'G'



sock = socket.socket()

with open("port_number", "r") as f:
    port = int(f.readline())

sock.bind(('0.0.0.0', port))

sock.listen(5)
with open("cmsg", "a") as log:
    fileLock = threading.Lock()
    while True:
        catSock = sock.accept()[0].makefile()
        #using sequential code instead or parallel
        #traffic is bounded to three messages total anyway
        #threading.Thread(target = receive, args = (catSock, log)).start()
        if receive(catSock, log):
            return
