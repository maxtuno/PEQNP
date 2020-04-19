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
from peqnp import *

if __name__ == '__main__':
    n = 10

    values = [random.random() for _ in range(n)]
    profit = [random.random() for _ in range(n)]

    capacity = sum(random.sample(values, k=n // 2))

    engine()

    selects = vector(is_mip=True, size=n)

    apply_single(selects, lambda x: x <= 1)

    assert dot(values, selects) <= capacity

    opt = maximize(dot(profit, selects))

    slots = list(map(int, selects))

    print('PROFIT  : {} vs {}'.format(dot(profit, slots), opt))
    print('VALUES  : {} <= {}'.format(dot(values, slots), capacity))
    print('SELECT  : {}'.format(slots))
