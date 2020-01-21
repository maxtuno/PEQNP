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
    return n_, mat


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the k-clique problem')
        print('Usage   : python3 k-clq.py <instance> <bits>')
        print('Example : python3 k-clq.py data.clq 10')
        exit(0)

    # Get the adjacent matrix and the dimension for the graph
    n, matrix = load_file(sys.argv[1])
    # Ths bits of the clique to search
    size = int(sys.argv[2])

    # Ensure the problem can be represented
    engine(bits=size.bit_length())

    # Declare an integer of n-bits
    bits = integer(bits=n)

    # The bits integer have "bits"-active bits, i.e, the clique has "bits"-elements
    assert sum(switch(bits, i) for i in range(n)) == size

    # This entangle all elements that are joined together
    for i in range(n - 1):
        for j in range(i + 1, n):
            if (i, j) not in matrix and (j, i) not in matrix:
                assert switch(bits, i) + switch(bits, j) <= 1

    # Get the first solution with turbo
    # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
    # only one solution is possible, because the internal structure of the problem is destroyed
    if satisfy(turbo=True):
        print(size)
        print(' '.join([str(i) for i in range(n) if not bits.binary[i]]))
    else:
        print('Infeasible ...')
