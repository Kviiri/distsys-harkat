import socket
import selectors
import sys
import random as rng

select = selectors.DefaultSelector()
if (len(argv) != 3):
    raise TypeError('Wrong number of arguments!')

confpath = argv[1]
confline = int(argv[2])
with open(confpath, 'r') as conf:
    conflines = conf.readlines()

inbox = socket.socket(type = socket.SOCK_DGRAM)
outbox = socket.socket(type = socket.SOCK_DGRAM)
outports = []
first = False
for i in range(0, len(conflines)):
    line = conflines[i].split()
    if (i == confline):
        id = line[0]
        inbox.bind(("localhost", int(line[1])))
        if(i == 0):
            first = True
    else:
        outports.append((line[0], int(line[1])))

try:
    log = open(id + ".log", "a")
except NameError as e:
    print "id is not defined: " + e.strerror
except IOError as e:
    print "error opening log file: " + e.strerror


#now we have the following:
#outports contains tuples (id, port) for other nodes

#inbox is listening the specified port
#outbox is unbound - it'll be used for sending messages

#log is the log file, named <id>.log

#first node pings others until everyone's up

if (first):
    inbox.settimeout(2)
    readyPorts = []
    while (len(readyPorts) != len(outports)):
        for port in outports:
            if port[1] in readyPorts:
                continue
            outbox.sendto("PING:" + str(id), ("localhost", port[1]))
        try:
            while True:
                reply = s.recv(128)
                readyPorts.append(int(reply))
        except socket.timeout:
            #if timeout is exceeded, we simply pass
            pass
    #all ports ready - time to start the algorithm
    for port in readyPorts:
        outbox.sendTo("START", ("localhost", port))

#others than first node wait for PING to let the first know they're ready
else:
    message = inbox.recv(128).split(":")
    if message[0] == "PING":
        replyto = outports[message[1]] #where to reply to
        outbox.sendto(str(id), ("localhost", replyto))
    

def __init__(hostname, port, outports, id):
    self.hostname = hostname
    self.id = id
    self.s = socket.socket(type = socket.SOCK_DGRAM)
    self.s.bind((hostname, port))
    self.o = socket.socket(type = socket.SOCK_DGRAM)
    self.outports = outports
    self.clock = 0    
    self.active = True
    startReceiving()

    
def start(self):
    self.log = open(id + ".log", "a")
    for i in range(1, 100):
        if(rng.randint(0, 1) == 0):
            localEvent()
        else:
            sendMessage()
    self.log.close()
        

def localEvent(self):
    increment = rng.randint(1,5)
    self.clock += increment
    self.log.write("l " + increment)

def sendMessage(self):
    target = outports[rng.choice(outports)]
    message = self.id + ":" + str(self.clock)
    self.o.sendto(message, ((self.hostname, target[1])))
    self.log.write("s " + target[0] + " " + self.clock)

def startReceiving(self):
    while(self.active):
       msg = self.s.recv(128).split(":")
       sender = msg[0]
       self.clock = max(self.clock, int(msg[1])) + 1
       self.log.write("r " + sender + " " + int(msg[1]) + " " + self.clock)

