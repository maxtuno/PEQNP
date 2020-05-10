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
import random
import numpy

if __name__ == '__main__':

    m = int(sys.argv[1])
    n = int(sys.argv[2])

    matrix = numpy.random.randint(-n, m, size=(n, m)) / numpy.random.logistic(size=(n, m))
    bb = numpy.random.randint(-n, n ** 2, size=(n,))
    cc = numpy.random.randint(-n, m, size=(m,)) / numpy.random.normal(size=(m,))

    bounds = []

    mmm = []
    bbb = []

    for e, row in enumerate(matrix):
        bbb.append(bb[e])
        mmm.append(row.tolist())

    for x in range(len(cc)):
        for y in range(len(cc)):
            if x == y:
                bounds.append(numpy.random.randint(1, m * n))
        bbb.append(bounds[-1])

    for x in range(len(cc)):
        kk = len(cc) * [0]
        kk[x] = 1
        mmm.append(kk)

    mode = random.choice(['min', 'max'])

    with open('mip_instance.py', 'w') as lp_file:
        print('import peqnp as pn\n', file=lp_file)
        print('pn.engine()\n', file=lp_file)

        for x in range(len(cc)):
            print('x{} = pn.linear()'.format(x), file=lp_file)

        for e, row in enumerate(matrix):
            print('assert ' + ' '.join('{}{:.4f} * x{}'.format('-' if c < 0 else '+', abs(c), x) for x, c in enumerate(row)) + ' <= {:.4f}'.format(bb[e]), file=lp_file)

        for x in range(len(cc)):
            print('assert ' + '{}x{} <= {:.4f}'.format('-' if x < 0 else '', abs(x), bounds[x]), file=lp_file)

        print('print(pn.{}('.format('minimize' if mode == 'min' else 'maximize', ) + ' '.join('{}{:.4f} * x{}'.format('-' if c < 0 else '+', abs(c), x) for x, c in enumerate(cc)) + '))', file=lp_file)

        for x in range(len(cc)):
            print('print(x{})'.format(x), file=lp_file)

    with open('mip_instance.lp', 'w') as lp_file:
        print('{}: '.format(mode) + ' '.join('{:.4f} * x{}'.format(c, x) for x, c in enumerate(cc)) + ';', file=lp_file)
        for e, row in enumerate(matrix):
            print(' '.join('{:.4f} * x{}'.format(c, x) for x, c in enumerate(row)) + ' <= {:.4f}'.format(bb[e]) + ';', file=lp_file)

        for x in range(len(cc)):
            print('x{} <= {:.4f};'.format(x, bounds[x]), file=lp_file)

        for x in range(len(cc)):
            print('int x{};'.format(x), file=lp_file)
