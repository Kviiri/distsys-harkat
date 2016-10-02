import socket
#import selectors
import sys
import random as rng
import threading

#select = selectors.DefaultSelector()
argv = sys.argv
if (len(argv) != 3):
    raise TypeError('Wrong number of arguments!')

confpath = argv[1]
confline = int(argv[2])
with open(confpath, 'r') as conf:
    conflines = conf.readlines()

outports = {} 
#connections = []
#ownLineFound = False
first = False
inbox = socket.socket(type = socket.SOCK_DGRAM)
outbox = socket.socket(type = socket.SOCK_DGRAM)
for i in range(0, len(conflines)):
    line = conflines[i].split()
    if (i == confline):
        inbox.bind(("localhost", int(line[1])))
        id = line[0]
        #ownLineFound = True
        #every node tries to connect to all nodes after it
        #first node doesn't listen, last node doesn't connect to outside
        #if i != 0:
        #    listener = socket.socket()
        if i == 0:
            first = True
    else:
        outports[line[0]] = int(line[1])
        #if ownLineFound:
        #    newSocket = socket.socket()
        #    connections.append((id, newSocket))


try:
    log = open(id + ".log", "a")
except NameError as e:
    print "id is not defined: " + e.strerror
except IOError as e:
    print "error opening log file: " + e.strerror


#now we have the following:
#outports contains tuples (id, port) for other nodes
#connections contains OUTGOING connection sockets for nodes (only latter ones)
#listener is the listening socket

#inbox is listening the specified port
#outbox is unbound - it'll be used for sending messages

#log is the log file, named <id>.log

#create the connections.
#each socket except the first begins listening

#if confline != 0:
#    listener.listen(512)
#
#while (len(connections) != len(outports)):
#    for id in outports.keys():
#        try:
#            newconn = socket.socket()
#            newconn.connect(("localhost"), outports(id))
#        except socket.error as e:
#            continue #in case no one's listening yet, just ignore and retry later
#        connections.append((id, newconn))

print outports
print str(id)

clock = 0
print "clock " + str(clock)


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
                print "waiting for reply"
                reply = inbox.recv(128)
                print "got reply from: " + reply
                if int(reply) not in readyPorts:
                    readyPorts.append(outports[reply])
        except socket.timeout:
            #if timeout is exceeded, we simply pass
            pass
    #all ports ready - time to start the algorithm
    for port in readyPorts:
        print "sending START!"
        outbox.sendto("START", ("localhost", port))

#others than first node wait for PING to let the first know they're ready
else:
    message = inbox.recv(128).split(":")
    if message[0] == "PING":
        print "got ping!"
        replyto = outports[message[1]] #where to reply to
        outbox.sendto(str(id), ("localhost", replyto))
    print "waiting for start"
    while True:
        message = inbox.recv(128)
        if message == 'START':
            inbox.settimeout(2)
            break
        else:
            print message


def start():
    for i in range(1, 100):
        if(rng.randint(0, 1) == 0):
            localEvent()
        else:
            sendMessage()
    active = False
    log.close()
        

def localEvent():
    increment = rng.randint(1,5)
    global clock
    clockLock.acquire()
    clock += increment
    clockLock.release()
    fileLock.acquire()
    log.write("l " + str(increment) + "\n")
    fileLock.release()

def sendMessage():
    target = rng.choice(outports.keys())
    message = id + ":" + str(clock)
    outbox.sendto(message, (("localhost", outports[target])))
    fileLock.acquire()
    log.write("s " + target + " " + str(clock) + "\n")
    fileLock.release()

def startReceiving():
    while(active):
        try:
            msg = inbox.recv(128).split(":")
        except socket.timeout:
            continue
        sender = msg[0]
        global clock
        clockLock.acquire()
        clock = max(clock, int(msg[1])) + 1
        clockLock.release()
        fileLock.acquire()
        log.write("r " + sender + " " + msg[1] + " " + str(clock) + "\n")
        fileLock.release()

fileLock = threading.Lock()
clockLock = threading.Lock()
active = True
receiverThread = threading.Thread(target = startReceiving)
receiverThread.start()
start()
active = False
log.close()
