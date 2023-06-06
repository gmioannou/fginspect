import sys
import os
from .filegdb import FileGDB


def main():
    if len(sys.argv) != 2:
        print('Usage: fginspect filegdb')
        exit(1)
    else:
        fgdb = sys.argv[1]

    if not os.path.isdir(fgdb):
        print('The File geodatabase is missing...')
        exit(1)

    filegdb = FileGDB(fgdb)
    filegdb.process()
