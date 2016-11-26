import random
def main():
    print("Welcome to List processor!")
    alist = []
    while True:
        try:
            read = int(input("Please input a positive integer to add (0 exits): "))
            if read == 0:
                break
            elif read < 0:
                print("Please input positive integers only!")
                continue
        except ValueError:
            print("Only positive integers, please!")
            continue
        except SyntaxError:
            print("Your input was empty, use 0 to end.")
            continue
        alist.append(read)
    print("Your list: " + str(alist))
    print("Its sum: " + str(listsum(alist)))

    #we want to shuffle the list, but our shuffling code is unreliable.
    #we need to do a fair bit of error handling here to get a good outcome.
    copy = alist[:] #copy alist
    while True:
        shuffle(alist) #try shuffling alist
        if frequencies(alist) == frequencies(copy):
            break #if frequencies match, it's good
        #if frequencies don't match, we had duplication. Try again
        print("Detected duplication when shuffling, output was " + str(alist))
        alist = copy[:]
    print("Shuffled list: " + str(alist))
    #create a convolution sum list
    #blist[i] contains alist[i-1] + alist[i] + alist[i+1]
    #this is computed using listsum, so errors can happen...
    blist = []
    for i in range(1, len(alist)-1):
        blist.append(listsum(alist[i-1:i+2]))
    print("The convolution sum list is: " + str(blist))
    print("The ratio list is: " + str(ratiolist(alist[1:-1], blist)))


#computes the sum of the numbers on the given list.
#FAULT: this method simulates an old-fashioned 4-digit counter from the 1980's.
#This means integer over- or underflow between 9999 and 0 is possible.
#lists with sums at least 10000 or under 0 will get erroneous results.
def listsum(list):
    sum = 0
    for number in list:
        sum = (sum + number) % 10000 #integer overflow possible!
    return sum

#shuffles the input list to a random permutation
#FAULT: the algorithm simulates a non-safely implemented parallel algorithm.
#swapping of two elements a and b can result in a duplicating over b
#this error is detected by use of the frequency method
def shuffle(list):
    for i in range(0, len(list) - 2):
        swapindex = random.randint(i, len(list) - 1)
        temp = list[swapindex]
        if(random.random() < 0.2):
            temp = list[i] #1/20 chance of accidentally duplicating
        list[swapindex] = list[i]
        list[i] = temp

#returns a dict with keys being numbers of the list and values their frequency.
#no fault - this simulates a dirty but effective detector for shuffle errors.
#we use frequencies as an indicator of a faulty shuffle, whenever it occurs
def frequencies(list):
    freq = {}
    for i in list:
        if i not in freq:
            freq[i] = 0
        freq[i] += 1
    return freq

#for each index in alist, returns alist[i] squared divided by blist[i]
#FAULT: naively assumes that blist contains only nonzero elements.
#will lead to division by zero error if blist does contain zeroes.
def ratiolist(alist, blist):
    ret = []
    for i in range(0, len(alist)):
        ret.append(alist[i] * alist[i] / blist[i])
    return ret

#runs the main method
main()
