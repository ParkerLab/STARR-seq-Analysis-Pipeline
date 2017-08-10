#!/usr/bin/env python

from __future__ import print_function

import argparse
import csv
import gzip
import sys

import leveldb


def open_maybe_gzipped(filename):
    """
    Open a possibly gzipped file.

    Parameters
    ----------
    filename: str
        The name of the file to open.

    Returns
    -------
    file
        An open file object.
    """
    with open(filename, 'rb') as test_read:
        byte1, byte2 = ord(test_read.read(1)), ord(test_read.read(1))
        if byte1 == 0x1f and byte2 == 0x8b:
            f = gzip.open(filename, mode='rt')
        else:
            f = open(filename, 'rt')
    return f


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='level',
        description='Create a LevelDB database with keys and values read from a file.'
    )
    parser.add_argument('database', help="""The name of the LevelDB database to access.""")
    parser.add_argument('source', nargs='?', help="""The name of the input file. Omit to read standard input.""")

    return parser.parse_args()

def perr(msg):
    print(msg, file=sys.stderr)

def pout(message):
    print(message, file=sys.stdout)

if __name__ == '__main__':
    args = parse_arguments()

    if args.source:
        source = open_maybe_gzipped(args.source)
    else:
        source = sys.stdin
    
    reader = csv.reader(source, delimiter='\t')
    db = leveldb.LevelDB(args.database)

    for count, (key, value) in enumerate(reader, 1):
        try:
            c = db.Get(key.encode('UTF-8')).decode('UTF-8')
            pout("{}\t{}".format(key, c))
        except KeyError as e:
            pout("{}\t{}".format(key, 0))
