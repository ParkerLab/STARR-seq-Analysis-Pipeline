#!/usr/bin/env python

from __future__ import print_function

import argparse
import csv
import gzip
import os.path
import shutil
import sys
import time

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
    parser.add_argument('-f', '--format', choices=['csv', 'tsv'], default='csv', help="""Specified the format of the input: csv for comma-separated values, tsv for tab-separated.""")
    parser.add_argument('database', help="""The name of the LevelDB database to create.""")
    parser.add_argument('source', nargs='?', help="""The name of the input file. Omit to read standard input.""")

    return parser.parse_args()


def perr(msg):
    print(msg, file=sys.stderr)


if __name__ == '__main__':
    args = parse_arguments()
    if args.source:
        source = open_maybe_gzipped(args.source)
    else:
        source = sys.stdin

    dialect = args.format == 'csv' and 'excel' or 'excel-tab'
    reader = csv.reader(source, dialect=dialect)

    if os.path.exists(args.database):
        perr('Database {} already exists.'.format(args.database))
        sys.exit(1)

    try:
        start = time.time()
        db = leveldb.LevelDB(args.database)
        for count, (key, value) in enumerate(reader, 1):
            db.Put(key.encode('UTF-8'), value.encode('UTF-8'))
            elapsed = (time.time() - start)
            rate = int(count / elapsed)
            if count % 10000 == 0:
                perr('{} records inserted in {} seconds ({}/sec)'.format(count, elapsed, rate))

    except ValueError as e:
        perr('Error: {}'.format(e))
        if 'unpack' in str(e):
            other_format = args.format == 'csv' and 'tsv' or 'csv'
            perr('You probably need to specify the input format as {}.'.format(other_format))
        perr('Removing database {}'.format(args.database))
        shutil.rmtree(args.database)
