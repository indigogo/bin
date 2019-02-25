#!/usr/bin/python

import string
from sys import argv,stderr
from os import popen
#from whrandom import random
import sys

def Help():
    print '\n'+'-'*75
    print 'usage: %s <silent-file> <out-file-prefix> <number-to-choose>\n'%argv[0]
    print '-'*75
    print '\n'
    sys.exit(0)
    return

if len(argv) != 4:
    Help()

in_file = argv[1]
out_file_prefix = argv[2]
choose = int(argv[3])

#########################

lines = map(string.split,
            popen('grep "SCORE" '+in_file+ " | grep -v \" score \" ").readlines()[1:]) ## skip header
N = len(lines)

n_files = (N -1) / choose + 1
#print n_files, choose

data = open(in_file,'r')
##first line, sequence
line = data.readline()
for i_file in range(1,n_files+1):
    out_file = out_file_prefix + ("_%04d"%i_file) + ".out"
    print out_file
    out = open(out_file,'w')
    out.write(line)
    out.close()
    
##second line, score header
line = data.readline()
#print line
for i_file in range(1,n_files+1):
    out_file = out_file_prefix + ("_%04d"%i_file) + ".out"
    out = open(out_file,'a')
    out.write(line)
    
i_file = 1
counter = 0
out_file = out_file_prefix + ("_%04d"%i_file) + ".out"
out = open(out_file,'a')

line = data.readline()
while (line):
    if line[:5] == 'SCORE':
        counter = counter + 1
        if counter > choose:
            out.close()
            
            counter = counter - choose
            i_file = i_file + 1
            out_file = out_file_prefix + ("_%04d"%i_file) + ".out"
            out = open(out_file,'a')
        
    out.write(line)
    line = data.readline()
data.close()
out.close()
