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

import sys

from peqnp import *

glb = 0


# The oracle for the problem, this count the satisfied clauses from the current assignment
def oracle(seq):
    global glb
    trail = [+(i + 1) if bit else -(i + 1) for i, bit in enumerate(seq)]
    loc = 0
    for cls in cnf:
        for lit in cls:
            if lit in trail:
                loc += 1
                break
    if loc > glb:
        glb = loc
        print('{} OF {} CLAUSES FROM {} THEORETICAL LIMIT FOR A POLYNOMIAL ALGORITHM'.format(glb, m, 7 * m // 8))
    return m - loc


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Approximate the max-sat problem')
        print('Usage   : python3 maxsat.py <cnf>')
        print('Example : python3 maxsat test.cnf')
        exit(0)

    # Load the instance
    n, m, cnf = 0, 0, []
    with open(sys.argv[1], 'r') as cnf_file:
        lines = cnf_file.readlines()
        for line in filter(lambda x: not x.startswith('c'), lines):
            if line.startswith('p cnf'):
                n, m = list(map(int, line[6:].split(' ')))
            else:
                cnf.append(list(map(int, line.rstrip('\n')[:-2].split(' '))))

    # Call hess algorithm to get a approximate solution
    seq = hess_binary(n, oracle=oracle, fast=True)

    # if the total clauses satisfied is equal to all clauses the problem is solved.
    if m == oracle(seq):
        print('s OPTIMUM FOUND')
    else:
        if m - oracle(seq) >= 7 * m // 8:
            print('c INSIDE INAPPROXIMABILITY RATIO')
        else:
            print('c ERROR: OUT OF INAPPROXIMABILITY RATIO')
    print(' '.join([str(+(i + 1) if bit else -(i + 1)) for i, bit in enumerate(seq)]) + ' 0')
