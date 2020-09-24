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

    # Get all python files in project path
    file_lst = python_files(os.path.abspath(os.getcwd()))

    # Convert to relative path
    file_lst = [ os.path.relpath(f) for f in file_lst ]

    # Gather todos from all files
    todos = []
    for f in file_lst:
        todos.extend(todos_in_file(f))

    print_todos(todos)

def python_files(path):
    """Return all files recursively starting at given path"""

    children = [ os.path.join(path, child) for child in os.listdir(path) ]
    subfiles = ( child for child in children if os.path.isfile(child) )
    subdirs  = ( child for child in children if os.path.isdir(child) )

    # Create list of python files
    lst = []

    # Add every file that ends with .py to list
    reg = re.compile('\.py$', re.IGNORECASE)
    for f in subfiles:
        if not re.search(reg, f):
            continue
        lst.append(f)

    # Recursively call this function and add all of its files to list
    for d in subdirs:
        lst.extend(python_files(d))

    return lst

def todos_in_file(path):
    """Retrieve all todos from given file as list of dicts"""

    # Read file line by line
    with open(path) as f:
        content = f.readlines()

    # Create list of dicts (representing todo entries)
    todos = []
    for number, line in enumerate(content):
        reg = re.compile('[ \t]*#[ \t]*TODO[: \n].*$', re.IGNORECASE)
        match = re.search(reg, line)
        if match:
            todos.append({ 'file': path,
                           'linenumber': number,
                           'text': match.group(0).strip() })

    return todos

def print_todos(todos):
    """Print dict of todos to stdout"""

    # Determine length of file names to pad to
    l = 0
    for todo in todos:
        l2 = len(todo['file'] + ':' + str(todo['linenumber']))
        if l2 > l:
            l = l2

    # Add padding (spaces) to the right
    pad = lambda s: s.ljust(l, ' ')
    strings = []
    for todo in todos:
        prefix = pad(todo['file'] + ':' + str(todo['linenumber']))
        suffix = todo['text']

        strings.append((prefix, suffix))

    # Print with padding applied
    for s in strings:
        print('{}    {}'.format(s[0], s[1]))

if __name__ == '__main__':
    sys.exit(main())
