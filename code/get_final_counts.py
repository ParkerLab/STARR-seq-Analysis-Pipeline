#!/usr/bin/env python
from __future__ import print_function
from itertools import izip
import gzip
import argparse
import sys

def pout(m):
    print(m, file=sys.stdout)

def create_counts(counts_f, duplicates_f):
    for count, dup in izip(gzip.open(counts_f), gzip.open(duplicates_f)):
        count = count.split()
        dup = dup.split()

        dup[1] = int(dup[1])
        count[1] = int(count[1])

        pout(count[0] + "\t" + str(count[1] - dup[1]))

def parse_arguments():
    parser = argparse.ArgumentParser('Specify duplicates and raw counts files.')
    parser.add_argument('-c', help='raw count filename')
    parser.add_argument('-d', help='duplicates filename')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    create_counts(args.c, args.d)
