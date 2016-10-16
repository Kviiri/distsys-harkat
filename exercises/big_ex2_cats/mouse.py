import sys
import socket

port = int(sys.argv[1])

sock = socket.socket()
sock.bind(('localhost', port))

sock.listen(5)

while True:
    print "ready"
    (replysock, replyto) = sock.accept()
    print "accepted"
    reply = replysock.makefile()
    #message format:
    msg = reply.readline().rstrip()
    print msg
    if msg == "MEOW":
        #oh dear, we got caught
        reply.write("OUCH\n")
        reply.flush()
        break


