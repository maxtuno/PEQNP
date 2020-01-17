"""
Copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import functools
import operator
import sys

from peqnp import *


def load_data(file_name):
    n_, m_, cnf_ = 0, 0, []
    with open(file_name, 'r') as cnf_file:
        lines = cnf_file.readlines()
        for line in filter(lambda x: not x.startswith('c'), lines):
            if line.startswith('p cnf'):
                n_, m_ = list(map(int, line[6:].split(' ')))
            else:
                cnf_.append(list(map(int, line.rstrip('\n')[:-2].split(' '))))
    return n_, m_, cnf_


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve SAT problem (re-encoded)')
        print('Usage   : python3 sat.py <cnf>')
        print('Example : python3 sat.py test.cnf')
        exit(0)

    n, m, cnf = load_data(sys.argv[1])

    engine(bits=2)

    x = integer(bits=n)

    for cls in cnf:
        assert functools.reduce(operator.ior, (switch(x, abs(lit) - 1, neg=lit > 0) for lit in cls)) > 0

    if satisfy(turbo=True):
        print('SAT')
        print(' '.join(map(str, [(i + 1) if b else -(i + 1) for i, b in enumerate(x.binary)])) + ' 0')
    else:
        print('UNSAT')
