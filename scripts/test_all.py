#!/usr/bin/env python3

import sys
import os
import unittest

# Relative path from this script to project directory
PROJECT_PATH = [ '..' ]

def main():
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner(buffer = True)
    test_suite = test_loader.discover('tests/')

    test_runner.run(test_suite)

if __name__ == '__main__':
    # cd to script directory
    os.chdir(os.path.dirname(sys.argv[0]))

    # cd to project directory
    for d in PROJECT_PATH:
        os.chdir(d)

    # Add cwd to pythonpath to enable importing of module
    cwd = os.path.abspath(os.getcwd())
    sys.path.append(cwd)

    sys.exit(main())
