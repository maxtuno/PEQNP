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

import random
import sys

from peqnp import *

# ref: https://cstheory.stackexchange.com/questions/16253/list-of-strongly-np-hard-problems-with-numerical-data
if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve Schur Triples Problem')
        print('Usage   : python3 schur-triples.py <bits> <bits>')
        print('Example : python3 schur-triples.py 7 10')
        exit(0)

    bits = int(sys.argv[1])
    size = 3 * int(sys.argv[2])

    triplets = []
    while len(triplets) < size:
        a = random.randint(1, 2 ** bits)
        b = random.randint(1, 2 ** bits)
        if a != b and a not in triplets and b not in triplets and a + b not in triplets:
            triplets += [a, b, a + b]
    triplets.sort()
    print(triplets)
    print()

    engine(bits=max(triplets).bit_length())

    xs, ys = permutations(triplets, size)

    for i in range(0, size, 3):
        assert ys[i] + ys[i + 1] == ys[i + 2]

    if satisfy(turbo=True, log=True):
        for i in range(0, size, 3):
            print('{} == {} + {}'.format(ys[i + 2], ys[i], ys[i + 1]))
    else:
        print('Infeasible ...')
