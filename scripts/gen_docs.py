#!/usr/bin/env python3

import sys
import os
import subprocess

# Relative path from this script to project directory
DOC_PATH = [ '..', 'docs' ]

# Relative path under DOC_PATH where documentation will be built
DOC_GEN_PATH = [ '_build', 'html' ]

def main():
    # cd to script directory
    os.chdir(os.path.dirname(sys.argv[0]))

    # cd to documentation directory
    for d in DOC_PATH:
        os.chdir(d)

    # Generate documentation
    try:
        gen_docs()
    except:
        return 1

    # cd to build directory
    for d in DOC_GEN_PATH:
        os.chdir(d)

    # Create .nojekyll file
    create_nojekyll()

    return 0

def gen_docs():
    """Generate docs at current directory"""

    print('Generating documentation with sphinx at {} ...'.format(os.getcwd()))

    # Decide which way to start sphinx depending on operating system
    if os.name == 'nt':
        generate_str = 'Make.bat html'
    else:
        generate_str = 'make html'

    subprocess.run(generate_str.split(' '), check = True)

def create_nojekyll():
    """Create empty .nojekyll file"""

    print('Creating .nojekyll file at {} ... '.format(os.getcwd()),
          end = '',
          flush = True)
    with open('.nojekyll', 'a'):
        pass
    print('done')

if __name__ == '__main__':
    sys.exit(main())
