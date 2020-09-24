#!/usr/bin/env python3

import sys
import os
import re

# Relative path from this script to source directory
SRC_PATH = [ '..', 'switchmng' ]

def main():
    # cd to script directory
    os.chdir(os.path.dirname(sys.argv[0]))

    # cd to source directory
    for d in SRC_PATH:
        os.chdir(d)

    # Start cleaning
    clear_dir(os.getcwd())

def clear_dir(path):
    # Go through directory children
    children = ( os.path.abspath(os.path.join(path, d)) for d in os.listdir(path) )
    children = ( d for d in children if os.path.isdir(d) )
    for d in children:
        if os.path.basename(d) == '__pycache__':
            delete_pycache(d)
        else:
            clear_dir(d)

def delete_pycache(path):
    delete_dir = True

    # Remove all *.py children files
    print('Deleting {}'.format(os.path.join(path, '*.pyc')))
    children = ( os.path.abspath(os.path.join(path, d)) for d in os.listdir(path) )

    for f in children:
        # Ignore symlinks and non regular files
        if os.path.islink(f) or not os.path.isfile(f):
            print('  Will not remove non regular file "{}"'.format(os.path.basename(f)))
            delete_dir = False
            continue

        # Ignore files not ending in .pyc
        reg = re.compile('\.pyc$', re.IGNORECASE)
        if not re.search(reg, os.path.basename(f)):
            print('  Will not remove non python cache file "{}"'.format(os.path.basename(f)))
            delete_dir = False
            continue

        # Delete .pyc files
        os.remove(f)

    # If we did not leave any files in __pycache__ directory we
    # can delete the directory itself
    if delete_dir:
        os.rmdir(path)
        print('Deleting {}'.format(path))

if __name__ == '__main__':
    sys.exit(main())

