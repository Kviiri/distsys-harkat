import subprocess
import exceptions
import threading
import random
import time



#read cmsg, wait delay seconds if no more data to read
#sets mouse location, Jazzy & Catty found status
#ends when mouse is killed
def logwatch(log, delay):
    global mouseLocation
    with open(log, "r") as f:
        while True:
            line = f.readline().rstrip()
            if line: #if returned line is non-empty
                msg = line.split()
                #assume messages are correct
                if msg[0] == 'F':
                    #mouse found!
                    mouseLocation = msg[1]
                    if msg[2] == 'Jazzy':
                        jazzyFound.set()
                    elif msg[2] == 'Catty':
                        cattyFound.set()
                elif msg[0] == 'A':
                    #mouse is dead, feel free to exit
                    break

def hunt(nodes, name):
    global mouseLocation
    while True:
        #no need to hunt if this cat has already found the mouse
        if ((name == 'Jazzy' and jazzyFound.isSet())
            or (name == 'Catty' and cattyFound.isSet())):
            return
        #no more nodes to search
        if not nodes:
            return
        #if mouse's location is known, go there instead of popping, then return
        if mouseLocation is not None:
            subprocess.call(["ssh", mouseLocation, "python chase_cat.py S " + name])
            return
        #pop is thread safe, so no lock needed
        target = ukkonodes.pop()
        subprocess.call(["ssh", target, "python chase_cat.py S " + name])

with open("ukkonodes") as f:
    ukkonodes = f.read().splitlines()

with open("listy_location") as f:
    listyhost = f.readline().rstrip()

if listyhost in ukkonodes:
    raise RuntimeError("listy host must not be in the ukkonodes list")

mouseLocation = None

#open, then close cmsg
#this ensurs cmsg is empty and extant when the program is run
open("cmsg", "w").close()

#threading events for Jazzy and Catty having found the mouse
jazzyFound = threading.Event()
cattyFound = threading.Event()

#start the mouse
threading.Thread(target = subprocess.call,
        args = (["ssh", random.choice(ukkonodes), "python mouse.py"]))

#start Listy cat
threading.Thread(target = subprocess.call,
        args = (["ssh", listyhost, "python listy.py"]))

#start the logwatch
threading.Thread(target = logwatch, args = ("cmsg", 0.2)).start()
#start the chase cats
threading.Thread(target = hunt, args = (ukkonodes, 'Jazzy')).start()
threading.Thread(target = hunt, args = (ukkonodes, 'Catty')).start()
jazzyFound.wait()
cattyFound.wait()
#at this point, all that remains is sniping the mouse
subprocess.call(["ssh", mouseLocation, "python chase_cat.py A Jazzy"])
