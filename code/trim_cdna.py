#!/usr/bin/env python
from __future__ import print_function 
from Bio.Seq import Seq
from itertools import izip
import sys
import argparse
import gzip

"""
BASES = list of bases 
MUTATED_SEQUENCES = list of all constant sequences that are mutated 1 base.
BC_PLASMID_BACKBONE = the expected sequence of the constant
INDEX = start index of the constant sequence 
TOTAL_LEN = total length of the strand being sequenced.
"""
FWD_READ = str()
REV_READ = str()
BACKBONE_1 = str()
BACKBONE_2 = str()

def pout(message):
    print(message, file=sys.stdout)

def perr(message):
    print(message, file=sys.stderr)

def parse_arguments():
    """
    Parse arguments provided by the user.
    """
    parser = argparse.ArgumentParser('Specify read files and errors')
    parser.add_argument('-d', help="Levenshtein distance (substitution only) for constant sequences\
                        .")
    parser.add_argument('--read1', help='File containing read1 data in fastq format.')
    parser.add_argument('--read3', help='File containing read3 data in fastq format.')
    return parser.parse_args()

def reverse_complement(sequence):
    """
    Get sequence reverse complement.
    """
    return str(Seq(sequence).reverse_complement())

def trim_newline(line):
    """
    Remove the newline from the read.
    """
    return line[:-1]

def prep_read2(seq):
    """
    Prepare read2 through reverse complement, trimmed newline.
    """
    return reverse_complement(trim_newline(seq))

def sub_distance(s, t):
    """
    Edit distance (substitution only).
    """
    d = 0
    for i in range(0, len(t)):
        if t[i] != s[i]:
            d += 1
    return d

if __name__ == '__main__':
    args = parse_arguments()
    FWD_READ = args.read1
    REV_READ = args.read3

    counter = 0

    for fwd, rev in izip(gzip.open(FWD_READ), gzip.open(REV_READ)):
        if(counter % 4 == 1):
            fwd = trim_newline(fwd)
            barcode = fwd[0:16]
            umi = reverse_complement(rev[0:6])

            pout(barcode + umi)

            counter += 1
        else:
            counter += 1
