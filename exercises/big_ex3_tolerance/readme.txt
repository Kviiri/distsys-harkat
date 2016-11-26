Distributed System Exercise 3  --  Fault Tolerance
Kalle Viiri

Introduction
------------

In this assignment, I show three methods each plagued by a fault manifesting into a different type of error when these methods are used by our "list processing suite". These faults represent reasonably common issues in real life software environments.

Run the program as follows:

python faulty.py

The outline of the program is as follows:
 1) the program asks the user to input positive integers. These are added to a list
 2) once the user inputs zero, the list is displayed along with its sum
 3) the list is shuffled
 4) a convolution sum list is computed by summing adjacent numbers except for the first and the last items, for example [5, 4, 1, 2] sums to [10, 7]
 5) the ratio between items of alist squared and blist non-squared, excluding first and last items of alist, is computed


Faulty methods
--------------

listsum returns the sum of a list given as input. It (supposedly) interfaces with a 1980's mechanical counter device for reasons unknown. A peculiarity of this counter is that it only has space for four digits, and overflow from 9999 to 0 is possible (and underflow, vice versa). This fault causes no immediate error, but can cause lingering problems like over/underflow usually does.

shuffle shuffles the input list using the Fisher-Yates shuffle. However, simulating a poorly implemented parallel algorithm, there is a fault that can cause swapping of two elements instead result in one element simply replacing the other and being duplicated. This happens with 5% chance per swap. The issue has been noticed and there is a dirty but non-faulty workaround - such duplications are detected by counting frequencies of numbers on the original list and the shuffled version, and the shuffle is attempted again until the frequencies match. Errors caused by the fault are reported.

ratiolist takes two lists as input, and returns a list that contains the ratio of each element's square from the first list and the corresponding element of the second list. The fault is that there is no zero-checking, which can result in arithmetic errors when dividing by zero. This occurs rarely in our application, only in the event of integer overflow from listsum, which would explain why it has flown under the radar. There is no check for such error, meaning that the user trying out the program can get a face full of stack trace as the program terminates.


In addition, there are two (hopefully) non-faulty methods: frequencies which is used for the work-around/error detection procedure of shuffle, and main which is simply the main method of the program.


Sample input for triggering the errors
--------------------------------------
listsum: 9000, 500, 500, 0  (causes sum to be zero instead of 10000, also triggers ratiolist error)
shuffle: no way to reliably trigger, but any sufficiently long list is likely to trigger it
ratiolist: 9000, 500, 500, 0 (also triggers listsum error earlier)
