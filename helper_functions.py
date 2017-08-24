from __future__ import print_function
import contextlib
import gzip
import functools
import itertools
import os
import re

def maybe_gzip(filename, ioniced=False):
    """Compress a file with gzip."""
    template_data = {
        'f': filename,
        'ionice': ioniced and 'ionice -c 2 -n 7 ' or ''
    }

    command_template = """if [ -r "{f}" ]; then {ionice}gzip -f "{f}"; elif [ -r "{f}".gz ]; then echo '"{f}" already gzipped.'; fi"""

    printp(command_template.format(**template_data))


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
        byte1, byte2 = test_read.read(1), test_read.read(1)
        if byte1 and ord(byte1) == 0x1f and byte2 and ord(byte2) == 0x8b:
            f = gzip.open(filename, mode='rt')
        else:
            f = open(filename, 'rt')
    return f

def rename_fastq(fastq, suffix=''):
    return FASTQ_RE.sub(fastq, suffix)

def make_read_group_header(library, id):
    read_group_components = {
        'ID': '{}___{}'.format(library['library'], id),

        # library
        'LB': library['library'],

        # sample
        'SM': library['sample'],

        # sequencing center name
        'CN': library['sequencing_center'],

        # ISO8601 date(time) of sequencing
        'DT': library['sequencing_date'],

        # platform (Illumina, Solid, etc. -- see the spec for valid values
        'PL': library['sequencing_platform'],

        # free-form description
        'DS': library['description'].replace('\n', ' '),
    }

    header = """@RG\\t{}""".format('\\t'.join('{}:{}'.format(k, v) for k, v in sorted(read_group_components.items()) if v))

    return header


def make_read_group_file(library_name, readgroup, suffix=''):
    return '{library_name}___{readgroup}{suffix}'.format(**locals())

def libraries_by_genome():
    libraries = {}
    for genome in library_reference_genomes():
        libraries[genome] = [library for library_name, library in sorted(LIBRARIES.items()) if library['reference_genome'] == genome]

    # return genome, libraries for each genom
    return sorted(libraries.items())



def iterate_library_files(library_name):
    """Generates a list of the library's files in DATA_PATH."""
    library = LIBRARIES[library_name]
    for rg, files in sorted(library['readgroups'].items()):
        for f in sorted(files):
            yield os.path.join(DATA_PATH, os.path.basename(f))