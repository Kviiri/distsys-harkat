A Tale of Cats and a Mouse
Distsys Big Exercise 2

By: Kalle Viiri

Contents:
#########

cordy.py - coordination
mouse.py - the target
chase_cat.py - search agents
listy.py - communication
readme - this file


HOW TO RUN
##########

1) Place the .py files above on an available Ukko node in your home dir
2) Create the following files:
 - ukkonodes: list of nodes to run the scripts on, one per line
 - listy_location: location of listy_cat (must not be included in ukkonodes)
 - port_number: the port for communication between the scripts
3) python cordy.py
4) [OPTIONAL] tail -f cmsg  to see the messages accumulate


DESCRIPTION
###########

CORDY: Cordy launches the entire process. It reads the files "ukkonodes" and "listy_location", makes sure there's no overlap, and launches the mouse on a random Ukko node and Listy on the node specified in "listy_location". Then it launches two threads running the hunt function - one for Catty, one for Jazzy. The hunt function keeps launching chase_cat.py on ukkonodes until all nodes have been visited or until cordy learns that the mouse has been located.

Cordy keeps track of the situation with another thread that constantly polls cmsg for new events from Listy. These events are used to update the two Event locks that allows Jazzy to launch the final attack on the mouse. In the sad but inevitable event of the mouse's passing, the thread ends.


MOUSE: This tasty rodent has little free will of its own. It is initially sent to a random eligible node by Cordy, and there it listens to localhost on the port specified in "port_number" file. Then it listens for connections, allowing Catty and Jazzy to know of its presence by trying to connect to its port. The mouse will also respond to the message "MEOW" with an appropriate "OUCH\n" and terminates afterwards.

To manually launch the mouse, python mouse.py


CATTY and JAZZY: These two are launched by Cordy on each Ukko node, only one cat per node (until the mouse is found). They have two modes: search (S) and destroy (A), determined by a command line flag. They are launched over ssh, and connect to localhost of the remote node where they're ordered. There, they attempt to connect to the port specified in "port_number". If the connection goes through, the mouse is found, and the cat reports this finding to Listy. To actually kill the mouse, the cat is launched separately with the A-command instead of the S-command, will send a MEOW message to the mouse, and report success (receiving OUCH) to Listy.

To manually launch Catty or Jazzy, python chase_cat.py <command> <name>
where <command> is S for search, A is for attack, and <name> is Catty or Jazzy.

Messages to Listy per the assignment: "F ukkoXXX Jazzy" indicates Jazzy found the mouse on node ukkoXXX. "G ukkoXXX Jazzy" indicates Jazzy killed the mouse on node ukkoXXX.


LISTY: This cat is placed (by Cordy) on the host specified in "listy_location". Listy acts as a very simple messenger, taking messages from the two chase cats and writing them to cmsg for Cordy to read. Due to the low volume of message traffic, Listy operates sequentially instead of in multithreaded mode.


NOTES
#####

- Tested to work on Ukko with Python 2.7.3 (default Python on Ukko)

- Ukko nodes are known to be a tad wonky, if one set of nodes doesn't work please try with a different set of nodes (or prune out the ones that break connections)

- Amazing ASCII art of Jazzy the cat in action below
 ______
< MEOW >
 ------
  \
   \ ,   _ ___.--'''`--''//-,-_--_.
      \`"' ` || \\ \ \\/ / // / ,-\\`,_
     /'`  \ \ || Y  | \|/ / // / - |__ `-,
    /@"\  ` \ `\ |  | ||/ // | \/  \  `-._`-,_.,
   /  _.-. `.-\,___/\ _/|_/_\_\/|_/ |     `-._._)
   `-'``/  /  |  // \__/\__  /  \__/ \
        `-'  /-\/  | -|   \__ \   |-' |
          __/\ / _/ \/ __,-'   ) ,' _|'
         (((__/(((_.' ((___..-'((__,'
