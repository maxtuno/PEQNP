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

import numpy as np
from peqnp import *

if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the 01 integer programming problem')
        print('Usage   : python3 01-integer-programming.py <bits> <matrix-dimension-1> <matrix-dimension-2>')
        print('Example : python3 01-integer-programming.py 15 5 10')
        exit(0)

    # the bits bits for the elements on the matrix
    bits = int(sys.argv[1])

    # the dimensions of the matrix
    n, m = int(sys.argv[2]), int(sys.argv[3])

    # The matrix
    cc = np.random.randint(0, 2 ** bits, size=(n, m))
    # Ensure that solution exist (for gen some interesting example)
    d = np.dot(cc, np.random.randint(0, 2, size=(m,)))

    print(cc)
    print(d)

    # Setup the engine with the bits of the sum of all values of the matrix, this ensure that the entire problem is well represented represented on the system.
    engine(bits=int(np.sum(cc)).bit_length())

    # Declare a [m] bit tensor
    x = tensor(dimensions=[m])

    # The main constrain for the problem (there is a one of the Karp's 21 NP-complete problems https://people.eecs.berkeley.edu/~luca/cs172/karp.pdf)
    assert (np.dot(cc, [x[[i]](0, 1) for i in range(m)]) == d).all()

    # Get the first solution with turbo
    # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
    # only one solution is possible, because the internal structure of the problem is destroyed
    if satisfy(turbo=True, boost=True):
        x = np.vectorize(int)(x.binary)
        print(x)
        print(np.dot(cc, x))
    else:
        print('Infeasible...')
