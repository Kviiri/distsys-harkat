import socket
import random as rng

class Node:

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

    def localEvent(self):
        increment = rng.randint(1,5)
        self.clock += increment
        self.log.write("l " + increment)

    def sendMessage(self):
        target = outports[rng.randint(0, outports.len)]
        message = self.id + ":" + str(self.clock)
        self.o.sendto(message, ((self.hostname, target)))

    def startReceiving(self):
        while(self.active):
            msg = self.s.recv(128).split(":")
            sender = msg[0]
            self.clock = max(self.clock, int(msg[1])) + 1
            self.log.write("r " + sender + " " + int(msg[1]) + " " + self.clock)

