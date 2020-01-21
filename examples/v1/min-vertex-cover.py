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


def load_file(file_name):
    mat = []
    with open(file_name, 'r') as file:
        for line in file.readlines():
            if line.startswith('p edge '):
                n_ = int(line[len('p edge '):].split(' ')[0])
            elif line.startswith('e '):
                x, y = map(int, line[len('e '):].split(' '))
                mat.append((x, y))
    xs, ys = zip(*mat)
    return n_, mat, sorted(set(xs + ys))


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the min-vertex cover problem')
        print('Usage   : python3 k-vertex-cover.py <instance>')
        print('Example : python3 k-vertex-cover.py data.clq')
        exit(0)

    # Get the nxn-matrix and dimension, and the bits of the cover.
    n, matrix, vertex = load_file(sys.argv[1])

    # Search for the min vertex cover
    opt = n
    while True:
        # Ensure the problem can be represented
        engine(bits=n.bit_length())

        # An integer with n-bits to store the indexes for the cover
        index = integer(bits=n)

        # This entangled the all possible covers
        for i, j in matrix:
            assert switch(index, vertex.index(i), neg=True) + switch(index, vertex.index(j), neg=True) >= 1

        # Ensure the cover has bits k
        assert sum(switch(index, vertex.index(i), neg=True) for i in vertex) < opt

        # Get the first solution with turbo
        # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
        # only one solution is possible, because the internal structure of the problem is destroyed
        if satisfy(turbo=True):
            opt = sum(index.binary)
            print('p bits {}'.format(opt))
            print(' '.join([str(vertex[i]) for i in range(n) if index.binary[i]]))
            print()
        else:
            break
