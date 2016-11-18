import random
def main():
    

#computes the sum of the numbers on the given list.
#FAULT: this method simulates an old-fashioned 4-digit counter from the 1980's.
#This means integer over- or underflow between 9999 and 0 is possible.
def listsum(list):
    sum = 0
    for number in list:
        sum = (sum + number) % 10000 #integer overflow possible!
    return sum

#shuffles the input list to a random permutation
#FAULT: the algorithm simulates a poorly implemented parallel data structure.
#swapping of two elements a and b can result in a duplicating over b
def shuffle(list):
    for i in range(0, len(list) - 1):
        swapindex = random.randint(i, len(list) - 1)
        temp = list[swapindex]
        if(random.random() < 0.001):
            temp = list[i] #1/1000 chance of accidentally duplicating
        list[swapindex] = list[i]
        list[i] = temp

#returns a dict with keys beign numbers of the list and values their frequency.
#no fault - this simulates a dirty but effective detector for shuffle errors.
def frequencies(list):
    freq = {}
    for i in list:
        if i not in freq:
            freq[i] = 0
        freq[i] += 1
    return freq

#for each index i of alist, checks if |alist[i]/blist[i]| <= ratio.
#returns True iff that check holds for all i, False otherwise.
#FAULT: naively assumes that blist contains only nonzero elements.
#will lead to division by zero if blist does contain zeroes.
def ratiolist(alist, blist, ratio):
    for i in enumerate(alist):
        if abs(alist[i] / blist[i]) > ratio:
            return False
    return True
