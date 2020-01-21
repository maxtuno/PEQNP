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

"""
This problem is a variation to proposed on https://twitter.com/hakankj/status/1219333235810938882 by Hakan Kjellerstrand
The main idea is given a sorted multi-set, their pair differences and one tip: an element and position for only one arbitrary element, is possible recovery the original multiset?
"""

import random
import time
import math
from peqnp import *


def generate(n, m):
    if m > n:
        print('m can ve <= that n')
        raise Exception('m > n')
    return sorted([random.randint(1, m) for _ in range(n)])


def pairs_difference(lst):
    return [abs(lst[i] - lst[j]) for i in range(len(lst)) for j in range(i + 1, len(lst))]


if __name__ == '__main__':

    original = generate(50, 25)

    # only one tip
    ith = random.choice(range(len(original)))
    tip = original[ith]

    diffs = pairs_difference(original)
    print('SIZE / DIFFERENCES : {} / {}'.format(len(diffs), diffs))
    print('SIZE / ORIGINAL    : {} / {}'.format(len(original), original))
    print('TIP                : {} at {}'.format(tip, ith))

    for n in range(math.ceil(math.sqrt(len(diffs))), len(diffs)):
        print(n)

        # init timer
        ini = time.time()

        # Empirical bits necessarily to solve the problem.
        engine(sum(diffs).bit_length() + 1)

        x = vector(size=n)

        # The tip is on x at index ith
        assert tip == index(ith, x)

        for i in range(n - 1):
            assert x[i + 1] >= x[i]

        xs = [one_of([x[i] - x[j], x[j] - x[i]]) for i in range(n) for j in range(i + 1, n)]

        for i in range(n):
            assert diffs[i] == xs[i]

        apply_single(x, lambda a: a <= max(diffs) + 1)

        # Solve the problem for only one solution.
        if satisfy(turbo=True):
            o = pairs_difference(list(map(int, x)))
            c = 100 * len(set(map(int, x)).intersection(set(original))) / len(set(original))
            print('SOLVED           : {}'.format(x))
            print('COINCIDENCES     : {}%'.format(c))
            if o == diffs:
                print('OK! - {}s'.format(time.time() - ini))
                break
            else:
                print('NOK! - {}s'.format(time.time() - ini))
                raise Exception('ERROR!')
