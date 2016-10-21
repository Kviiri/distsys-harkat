import sys
import time
import socket
from __future__ import print_function

if len(argv) != 3:
    print ("Wrong number of arguments: " + argv)
    return

#either S or A
action = argv[1]

#our name!
name = argv[2]

#we also need the port number
with open("port_number") as f:
    port_number = int(f.readline())


if name != "Jazzy" and name != "Catty":
    print ("I'm a stray cat! (name must be Jazzy or Catty)")
    return

if action == "S":
    #search the node
    if search(12):
        #found it!
        sock = listyConnect()
        #sock is a file-like socket for communicating with Listy cat
        print("F " + gethostname() + " " + name, file=sock)
        sock.flush()
elif action == "F":
    #off the rodent
    if destroy(6, 8):
        #mouse is dead. Rest in pieces
        #Listy must know of its passing
        sock = listyConnect()
        #sock is a file-like socket for communicating with Listy cat
        print("G " + gethostname() + " " + name, file=sock)
        sock.flush()

def search(searchTime):
    time.sleep(searchTime)
    sock = socket.socket()
    #found is False - set it to True if connection is successful
    found = False
    try:
        sock.connect(('localhost', port_number))
        #success?
        found = True
    except timeout:
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
    except timeout:
        return False
    #connection formed, mouse has waitTime seconds to reply
    try:
        sock.send("MEOW")
        msg = sock.recv(4)
    except timeout:
        return False
    if msg == "OUCH":
        return True
    

#helper function. Returns a socket connected to Listy cat
def listyConnect():
#first get Listy's location
    with open("listy_location") as f:
        listyhost = f.readline
    #then connect to Listy
    sock = socket()
    sock.connect(('listy_location'))
    sock = sock.makefile()
    return sock
