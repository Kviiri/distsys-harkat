README for Lamport Clocks Distsys Assignment 1
Kalle Viiri
013864453

RUNNING THE PROGRAM

python lamport_node.py <conf> <line>
where <conf> is the name of a configuration file
      <line> is the line of the configuration file applicable to this node (starting from 0)

The Lamport Clock algorithm will only start when all nodes specified in the conf file have been launched. The number of lines in the conf line should match the number of nodes desired.


OUTPUT

To standard output:
Local event: l <x>, where <x> is the increment of the clock done in the local event
Message out: s <r> <t>, where <r> is the recipient's ID and <t> is the sender's timestamp
Messages in: r <s> <t> <n>, where <s> is the sender, <t> is the received timestamp and <n> is the new timestamp assigned after processing the message


IMPLEMENTATION

Each node has two datagram sockets, inbox and outbox. After reading the input file, each knows the other nodes' ports. The first node of the configuration file pings other nodes until everyone has replied, after which the first node sends everyone a START message that allows other nodes to start the main algorithm.

The main algorithm is done in two threads: one processes incoming messages (normal or SIGNOFF) and the other carries out local events and sending events. Locks are in place for protecting the clock value and output from concurrency issues. When a node finishes its 100 events, it sends every other node a SIGNOFF message along with its ID. Nodes receiving a SIGNOFF message remove the associated id from the list of eligible nodes to send to. The final remaining node will perform only local events.
