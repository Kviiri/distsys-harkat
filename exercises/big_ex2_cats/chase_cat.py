from __future__ import print_function
import sys
import time
import socket
import exceptions

def search(searchTime):
    time.sleep(searchTime)
    sock = socket.socket()
    #found is False - set it to True if connection is successful
    found = False
    try:
        sock.connect(('localhost', port_number))
        #success?
        found = True
    except (socket.timeout, socket.error):
        #no mouse here
        pass
    return found

#sleeps killTime, then tries to kill mouse (MEOW)
#if it doesn't receive reply in waitTime seconds, ends
def destroy(killTime, waitTime):
    time.sleep(killTime)
    sock = socket.socket()
    sock.settimeout(waitTime)
    try:
        sock.connect(('localhost', port_number))
    except socket.timeout:
        return False
    #connection formed, mouse has waitTime seconds to reply
    try:
        print("MEOW", file=sock)
        msg = sock.recv(4)
    except (socket.timeout, socket.error):
        return False
    if msg == "OUCH":
        return True
    

#helper function. Returns a socket connected to Listy cat
def listyConnect():
#first get Listy's location
    with open("listy_location") as f:
        listyhost = f.readline().rstrip()
    #then connect to Listy
    sock = socket.create_connection((listyhost, port_number))
    sock = sock.makefile()
    return sock

if len(sys.argv) != 3:
    raise RuntimeError("Wrong number of arguments: " + " ".join(sys.argv))

#either S or A
action = sys.argv[1]

#our name!
name = sys.argv[2]

#we also need the port number
with open("port_number") as f:
    port_number = int(f.readline())


if name != "Jazzy" and name != "Catty":
    raise RuntimeError("I'm a stray cat! (name must be Jazzy or Catty)")

if action == "S":
    #search the node
    if search(12):
        #found it!
        sock = listyConnect()
        #sock is a file-like socket for communicating with Listy cat
        print("F " + socket.gethostname() + " " + name, file=sock)
        sock.flush()
elif action == "A":
    #off the rodent
    if destroy(6, 8):
        #mouse is dead. Rest in pieces
        #Listy must know of its passing
        sock = listyConnect()
        #sock is a file-like socket for communicating with Listy cat
        print("G " + gethostname() + " " + name, file=sock)
        sock.flush()


