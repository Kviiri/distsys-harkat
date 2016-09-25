import socket
import random as rng

class Node:

    def __init__(hostname, port, outports):
        self.s = socket.socket(type = socket.SOCK_DGRAM)
        self.s.bind((hostname, port))
        self.o = socket.socket(type = socket.SOCK_DGRAM)
        self.outports = outports
        self.clock = 0    
        self.active = True
        startReceiving()

    
    def start():
        for i in range(1, 100):
            if(rng.randint(0, 1) == 0):
                localEvent()
            else:
                sendMessage()

    def localEvent(self):
        self.clock += rng.randint(1,5);

    def sendMessage(self):


    def startReceiving(self):
        while(self.active):
            msg = self.s.recv(128)
            
