#!/usr/bin/env python
#
# This script gives an example for Spark assignments on the 
# Distributed systems course. Note that a Spark context depends on 
# specific platform and settings. Please modify this file and play
# with it to get familiar with Spark.
#
# Liang Wang @ CS Dept, Helsinki University, Finland
# 2015.01.19 (modified 2016.11.29, owaltari)
# 
# modified for personal submission
# 2016-12-15 kviiri (013864453)
#

import os
import sys
import math

### Dataset
DATA1 = '/cs/work/scratch/spark-data/data-1.txt'

### Some variables you may want to personalize
AppName = "example"
TMPDIR = "/cs/work/scratch/spark-tmp"

### Create a Spark context on Ukko cluster
from pyspark import SparkConf, SparkContext
conf = (SparkConf()
        .setMaster("spark://ukko007:7077")
        .setAppName(AppName)
        .set("spark.rdd.compress", "true")
        .set("spark.broadcast.compress", "true")
        .set("spark.cores.max", 10)  # do not be greedy :-)
        .set("spark.local.dir", TMPDIR))
sc = SparkContext(conf = conf)

### Put your algorithm here.

#simple sum/n
def calculate_average(data):
    return data.sum() / data.count()

#simple reduce call for max and min
def calculate_max(data):
    return data.reduce(lambda x, y: x if (x > y) else y)

def calculate_min(data):
    return data.reduce(lambda x, y: x if (x < y) else y)

#readymade variance function
def calculate_variance(data):
    return data.variance()

#slow histogram algorithm
def calculate_histograms(data, bins):
    #how large is each bin in the output?
    binsize = 100 / float(bins)
    for i in range(0, bins):
        #i * binsize is the lower bound for a bin
        #(i+1) * binsize is the upper bound
        print(str(data.filter(lambda x: i * binsize < x and x <= (i+1) * binsize).count()))

#fast histogram algorithm, maps values to buckets in single pass (per granularity level)
def calculate_buckets(data, bins):
    #using 1000 as the baseline for binsize
    #all numbers are scaled 10x so ceil works for inclusive upper bound
    binsize = 1000 / float(bins)
    data = data.map(lambda x: (math.ceil(x*10 / binsize), x))
    return data.countByKey()

if __name__=="__main__":
    #load the dataset from the text file only once
    data = sc.textFile(DATA1).map(lambda s: float(s))
    myAvg = calculate_average(data)
    print "Avg. = %.8f" % myAvg
    myMax = calculate_max(data)
    print "Max  = %.8f" % myMax
    myMin = calculate_min(data)
    print "Min  = %.8f" % myMin
    myVar = calculate_variance(data)
    print "Var. = %.8f" % myVar

    #in case someone tries to insert non-binnable numbers!
    data = data.filter(lambda x: x > 0 and x <= 100)
    data.cache() #cache so the filter operation's result is preserved
    for bincount in [10, 100, 1000]:
        with open('{}_histogram.txt'.format(bincount), 'w') as f:
            histograms = calculate_buckets(data, bincount)
            #this loop goes through the buckets
            for i in range(1, bincount + 1):
                if histograms[i]:
                    f.write(str(histograms[i]) + '\n')
                #if no key is found, then it's a zero
                else:
                    f.write('0\n')
    sys.exit(0)

