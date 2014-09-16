#!C:\Python27\python.exe

from __future__ import division
import re
import numpy
import mmap
import os
import math
import matplotlib.pyplot as plt
from pylab import *
import _mysql
import gc

def makeregex(wordlist):
    regex = []
    for i in range(len(wordlist)):
        regex.append("[ /r/t]+" + wordlist[i] + "[/]")
    return regex

def get_all_words():
    allwords = []
    for i in range(len(final)-1):
        size = os.stat(final[i]).st_size
        fil = open(final[i])
        if(fil):
            data = mmap.mmap(fil.fileno(), size, access = mmap.ACCESS_READ)
            t = re.findall(r"[ ]*[a-zA-Z]+[/]", data)
            allwords += [t[i].rstrip('/').lstrip(' ') for i in range(len(t))]
        fil.close()
    return list(set(allwords))

def get_word_count(wordlist, final):
    regex = []
    count = [[] for x in xrange(len(wordlist))]
    frequency = []
    total = []
    
    regex = makeregex(wordlist)
    
    for i in range(len(final)-1):
        size = os.stat(final[i]).st_size
        fil = open(final[i])
        if(fil):
            print final[i] + " read!"
            data = mmap.mmap(fil.fileno(), size, access=mmap.ACCESS_READ)
            for j in range (len(wordlist)):
                total.append(len(re.findall(r"[a-zA-Z]/[a-zA-Z]", data)))
                count[j].append(len(re.findall(regex[j], data)))            
        fil.close()

    for k in range(len(wordlist)):
        frequency.append(sum(count[k]))

    return frequency, sum(total)

##--------------------------------------------------##
gc.disable()
filename = "D:\\brown\\list.dat";
f = open(filename)
lines = f.readlines()
final = []
probability = []
constant = []

for i in range(len(lines)-1):
    final.append(lines[i].rstrip('\n'));

f.close()
## File lists stored in final-----------------------##

wordlist = get_all_words()
word_count_array = numpy.empty((len(wordlist), 4), dtype = numpy.object)
rank = [i+1 for i in range(len(wordlist))]
(frequency, total) = get_word_count(wordlist, final)

for i in range(len(wordlist)):
    probability.append('{:0.10f}'.format(frequency[i]/total))

for i in range(len(wordlist)):
    word_count_array[i, 0] = wordlist   [i]
    word_count_array[i, 1] = frequency  [i]
    word_count_array[i, 2] = probability[i]

idx = numpy.argsort(word_count_array[:, 1])
idx = idx[::-1]
word_count_array = word_count_array[idx]

for i in range(len(wordlist)):
    word_count_array[i, 3] = math.log1p(float(frequency[i] * (i+1)))

logfrequency = [math.log1p(float(i)) for i in word_count_array[:, 1]]
logrank      = [math.log1p(float(i)) for i in rank]

figure(1)
plot(logrank, logfrequency,'b')
title('Zipf\'s Law')
xlabel('log rank')
ylabel('log frequency')
savefig('zipf_log.png')
show()

figure(2)
plot(rank, word_count_array[:, 1], 'b')
title('Zipf\'s Law')
xlabel('rank')
ylabel('frequency')
savefig('zipf.png')
show()
