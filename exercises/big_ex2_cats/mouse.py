import sys
import socket

with open("port_number", "r") as f:
    port = int(f.readline().rstrip())

sock = socket.socket()
sock.bind(('localhost', port))

sock.listen(5)

while True:
    (replysock, replyto) = sock.accept()
    reply = replysock.makefile()
    #message format:
    msg = reply.readline().rstrip()
    print msg
    if msg == "MEOW":
        #oh dear, we got caught
        reply.write("OUCH\n")
        reply.flush()
        break
