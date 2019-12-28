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

    n = int(sys.argv[1])

    np.random.seed(n)

    matrix = np.random.randint(0, 2, size=(n, n))
    matrix -= np.identity(n, dtype=int) * np.diagonal(matrix)

    print(matrix)

    engine(2 * n.bit_length())

    indexes, elements = permutations((1 - matrix).tolist(), n)

    assert sum(elements) == 0

    if satisfy(turbo=True):
        for i in indexes:
            for j in indexes:
                sys.stdout.write('{} '.format(matrix[i.value][j.value]))
            print()
        print()
    else:
        print('Infeasible ...')
