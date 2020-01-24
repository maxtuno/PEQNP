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

import matplotlib.pyplot as plt
import numpy
from peqnp import *

numpy.random.seed(0)

glb = numpy.inf


def oracle(seq):
    global glb
    loc = sum(numpy.linalg.norm(data[seq[i]] - data[seq[(i + 1) % len(seq)]]) for i in range(n))
    if loc < glb:
        glb = loc
        print('Tour Length {}'.format(glb))
    return loc


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Approximate the TSP problem')
        print('Usage   : python3 tsp.py <bits>')
        print('Example : python3 tsp.py 100')
        exit(0)

    n = int(sys.argv[1])

    data = numpy.random.logistic(size=(n, 2))

    seq = hess_sequence(n, oracle=oracle, fast=True)

    x, y = zip(*[data[i] for i in seq + [seq[0]]])

    plt.title('PEQNP - www.peqnp.science')
    plt.plot(x, y, 'k-')
    plt.plot(x, y, 'r.')
    plt.savefig('tsp.png')
