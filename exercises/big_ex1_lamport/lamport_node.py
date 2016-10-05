import socket
import sys
import random as rng
import threading
import time

argv = sys.argv
if (len(argv) != 3):
    raise TypeError('Wrong number of arguments!')

confpath = argv[1]
confline = int(argv[2])
with open(confpath, 'r') as conf:
    conflines = conf.readlines()

outports = {} 
first = False
inbox = socket.socket(type = socket.SOCK_DGRAM)
outbox = socket.socket(type = socket.SOCK_DGRAM)
for i in range(0, len(conflines)):
    line = conflines[i].split()
    if (i == confline):
        inbox.bind(("localhost", int(line[1])))
        id = line[0]
        if i == 0:
            first = True
    else:
        outports[line[0]] = int(line[1])

#now we have the following:
#outports contains tuples (id, port) for other nodes

#inbox is listening the specified port
#outbox is unbound - it'll be used for sending messages

#clock is initialized
clock = 0

#first node pings everyone until everyone's replied
if (first):
    readyPorts = []
    while (len(readyPorts) != len(outports)):
        inbox.settimeout(2)
        for port in outports.values():
            if port in readyPorts:
                continue
            try:
                outbox.sendto("PING:" + str(id), ("localhost", port))
            except socket.error:
                pass
        try:
            while True:
                reply = inbox.recv(128)
                #if we hadn't got replies from this node yet, add them to ready ports
                if int(reply) not in readyPorts:
                    readyPorts.append(outports[reply])
        except socket.timeout:
            #if timeout is exceeded, we simply pass
            pass
    #all ports ready - time to start the algorithm
    for port in readyPorts:
        #send START to all, signifying that the first node is ready
        outbox.sendto("START", ("localhost", port))

#others than first node wait for PING to let the first know they're ready
else:
    message = inbox.recv(128).split(":")
    #PING got!
    if message[0] == "PING":
        replyto = outports[message[1]] #where to reply to
        outbox.sendto(str(id), ("localhost", replyto))
    while True:
        #wait for START
        message = inbox.recv(128)
        if message == 'START':
            inbox.settimeout(2)
            break
        else:
            print message

#next the methods of the Lamport clock algorithm
#start: starts the algorithm and executes for 100 steps
def start():
    for i in range(1, 100):
        #coinflip between local and send event
        #only local events happen if no other nodes are active
        if(rng.randint(0, 1) == 0) or not outports:
            localEvent()
        else:
            sendMessage()

#localevent: increments counter by 1, 2, 3, 4 or 5
def localEvent():
    #short sleep to simulate actually doing something locally
    time.sleep(0.05)
    increment = rng.randint(1,5)
    global clock
    clockLock.acquire()
    clock += increment
    clockLock.release()
    printLock.acquire()
    print "l " + str(increment)
    printLock.release()

#sendMessage: picks a random node from the remaining ones and sends a message
def sendMessage():
    global clock
    #uniformly random selection from ids to send to
    target = rng.choice(outports.keys()) 
    clockLock.acquire()
    clock += 1 #increment clock
    message = id + ":" + str(clock)
    outbox.sendto(message, (("localhost", outports[target])))
    printLock.acquire()
    print "s " + target + " " + str(clock)
    printLock.release()
    clockLock.release()

#startReceiving: executed in a separate thread
#receives both main messages and SIGNOFF messages
def startReceiving():
    while(active):
        try:
            msg = inbox.recv(128).split(":")
        except socket.timeout:
            continue
        #SIGNOFF messages remove the specified element from outports
        #format: SIGNOFF:<id>
        if msg[0] == "SIGNOFF":
            del outports[msg[1]]
            continue
        sender = msg[0]
        global clock
        clockLock.acquire()
        clock = max(clock, int(msg[1])) + 1
        clockLock.release()
        printLock.acquire()
        print "r " + sender + " " + msg[1] + " " + str(clock)
        printLock.release()


#fire up the algorithm
#printLock: locks printing for thread safety
#clockLock: locks clock for thread safety
printLock = threading.Lock()
clockLock = threading.Lock()
#active: True until 100 events have happened
active = True
#start a new thread for receiving messages
receiverThread = threading.Thread(target = startReceiving)
receiverThread.start()
#start the algorithm
start()
#after algorithm, this boolean lets receiver thread know it should terminate
active = False
#let everyone else know we no longer accept messages
for port in outports.values():
    outbox.sendto("SIGNOFF:" + id, ("localhost", port))
