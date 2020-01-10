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

import random
import time

from peqnp import *


# Permutation Reconstruction fromDifferences
# from https://arxiv.org/pdf/1410.6396.pdf

def gen_instance(n):
    y = list(range(1, n + 1))
    random.shuffle(y)
    return [abs(y[i - 1] - y[i]) for i in range(n)]


if __name__ == '__main__':

    for n in range(3, 100):
        ini = time.time()

        print('size : {}'.format(n))

        # Generate the problem
        diffs = gen_instance(n)

        # Because the largest number on the problem (with operations) is bits of n there is the necessarily bits for the engine and add 1 for the subtraction.
        engine(n.bit_length() + 1)

        # Declare a n-vector of integer variables to store the solution.
        x = vector(size=n)

        # All elements are different and from 1 to n there is a permutation.
        all_different(x)
        apply_single(x, lambda a: 1 <= a <= n)

        # The i-th element of the instance is the absolute difference of two consecutive elements
        for i in range(n):
            assert index(i, diffs) == one_of([x[i - 1] - x[i], x[i] - x[i - 1]])

        # Solve the problem for only one solution, according to the paper are two equivalents.
        if satisfy(turbo=True):
            xx = [abs(x[i - 1] - x[i]) for i in range(n)]
            if xx == diffs:
                print(x)
                print(xx)
                print('OK! - {}s'.format(time.time() - ini))
            else:
                raise Exception('Error!')
        else:
            raise Exception('Error!')
