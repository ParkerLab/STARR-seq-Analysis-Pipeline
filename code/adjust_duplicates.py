#!/usr/bin/env python
from __future__ import print_function 
import sys

def pout(message):
    print(message, file=sys.stdout)

if __name__ == '__main__':
    for line in sys.stdin:
        line = line.split()
        pout(line[0][0:16] + "\t" + str(int(line[1])-1))
