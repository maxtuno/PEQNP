"""
copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science

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

import numpy as np
from peqnp import *

if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the undirected hamiltonian cycle problem')
        print('Usage   : python3 hcp.py <adjacent-matrix-dimension>')
        print('Example : python3 hcp.py 10')
        exit(0)

    # The dimension of the nxn adjacent-matrix for the graph
    n = int(sys.argv[1])

    # Generate a 01 matrix
    matrix = np.random.randint(0, 2, size=(n, n))
    # Put 0s on diagonal
    matrix -= np.identity(n, dtype=int) * np.diagonal(matrix)

    # show thw matrix
    print(matrix)

    # Ensure that the problem can be full represented on the system.
    engine((n ** 2).bit_length())

    # Entangle all possible paths changing 0 <-> 1 i.e. 0 if edge exist 1 if not.
    indexes, elements = matrix_permutation((1 - matrix).tolist(), n)

    # The path is full, (all elements are joined).
    assert sum(elements) == 0

    # Get the first solution with turbo
    # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
    # only one solution is possible, because the internal structure of the problem is destroyed
    if satisfy(turbo=True):
        for i in indexes:
            for j in indexes:
                sys.stdout.write('{} '.format(matrix[i.value][j.value]))
            print()
        print()
    else:
        print('Infeasible ...')
