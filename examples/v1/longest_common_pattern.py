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
        print('Solve the longest common pattern (permutation) problem')
        print('Usage   : python3 longest_common_pattern.py <number-of-strings> <size_of_strings>')
        print('Example : python3 longest_common_pattern.py 5 10')
        exit(0)

    m, n = int(sys.argv[1]), int(sys.argv[2])

    mapping = {1: '-', n: 'A', n ** 2: 'C', n ** 3: 'T', n ** 4: 'G'}

    t, S = 0, []
    for i in range(m):
        S.append([n ** i for i in np.random.randint(1, 5, size=n)])
        t = max(t, np.sum(S[-1]))
        print(''.join([mapping[s] for s in S[-1]]))

    opt = 1
    while True:
        engine(int(t).bit_length())

        X = []
        for s in S:
            X.append(np.asarray(subset(s, k=n, empty=1)))

        apply_dual(X, lambda a, b: np.sum(a) == np.sum(b) > opt)

        if satisfy(turbo=True):
            print()
            opt = np.sum(X[-1])
            for x in X:
                print(''.join([mapping[int(x[i])] for i in range(n)]))
        else:
            break
