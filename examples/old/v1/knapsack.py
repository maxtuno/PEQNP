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

if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the knapsack problem')
        print('Usage   : python3 knapsack.py <bits> <bits>')
        print('Example : python3 knapsack.py 10 10')
        exit(0)

    b = int(sys.argv[1])
    n = int(sys.argv[2])

    costs = [random.randrange(1, 2 ** b) for _ in range(n)]
    profits = [random.randrange(1, 2 ** b) for _ in range(n)]
    capacity = sum(random.sample(costs, k=n // 2))

    print('n = {};'.format(n))
    print('bits = {};'.format(costs))
    print('profit = {};'.format(profits))
    print('capacity = {};'.format(capacity))

    print(80 * '-')

    # Search for the optimal
    p = 0
    while True:
        # Ensure the problem can be represented
        engine(max(sum(costs), sum(profits)).bit_length())

        # Get the subsets for the cost, sc is the binary representation (integer) for the subsets, and the sub_c is the entangled subset.
        sc, sub_c = subsets(costs)
        # Get the subsets for the profits, sp is the binary representation (integer) for the subsets, and the sub_p is the entangled subset.
        sp, sub_p = subsets(profits)

        # The main constraints capacity is not violated
        assert sum(sub_c) <= capacity
        # The current profit is greater than the current value
        assert sum(sub_p) > p
        # Ensure that the two subsets coincide by indexes
        assert sc == sp

        # Get the first solution with turbo
        # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
        # only one solution is possible, because the internal structure of the problem is destroyed
        if satisfy(turbo=True):
            ps = [profits[i] for i in range(n) if sp.binary[i]]
            cs = [costs[i] for i in range(n) if sc.binary[i]]
            p = sum(ps)
            c = sum(cs)
            print(p, ps)
            print(c, cs)
            print()
        else:
            break