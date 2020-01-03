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
import sys

from peqnp import *


def completion(n, m, seed):
    """
    http://www.csplib.org/Problems/prob079/data/queens-gen-fast.py.html
    """
    random.seed(seed)

    d1 = [0 for _ in range(2 * n - 1)]
    d2 = [0 for _ in range(2 * n - 1)]

    valid_rows = [i for i in range(n)]
    valid_cols = [j for j in range(n)]

    def no_attack(r, c):
        return d1[r + c] == 0 and d2[r - c + n - 1] == 0

    pc = []
    queens_left = n

    for attempt in range(n * n):
        i = random.randrange(queens_left)
        j = random.randrange(queens_left)
        r = valid_rows[i]
        c = valid_cols[j]
        if no_attack(r, c):
            pc.append([r, c])
            d1[r + c] = 1
            d2[r - c + n - 1] = 1
            valid_rows[i] = valid_rows[queens_left - 1]
            valid_cols[j] = valid_cols[queens_left - 1]
            queens_left -= 1
            if len(pc) == m:
                return [[x + 1, y + 1] for x, y in pc]


def save(pc):
    with open('nqc_{}_{}_{}.txt'.format(n, m, seed), 'w') as file:
        table = ''
        for i in range(1, n + 1):
            table += ''
            for j in range(1, n + 1):
                if [i, j] not in pc:
                    table += '. '
                else:
                    table += 'Q '
            table += '\n'
        print(table, file=file)
        print('# seed = {}'.format(seed), file=file)


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the n-queens-completion problem')
        print('Usage   : python3 n-queens-completion.py <table-size> <placed-queens>')
        print('Example : python3 n-queens-completion.py 100 50')
        exit(0)

    n, m, seed = int(sys.argv[1]), int(sys.argv[2]), random.random()

    placed_queens = completion(n, m, seed)

    save(placed_queens)

    engine(bits=n.bit_length() + 1)

    qs = vector(key='qs', size=n)

    for (a, b) in placed_queens:
        assert qs[a - 1] == b - 1

    apply_single(qs, lambda x: x < n)
    apply_dual(qs, lambda x, y: x != y)
    apply_dual([qs[i] + i for i in range(n)], lambda x, y: x != y)
    apply_dual([qs[i] - i for i in range(n)], lambda x, y: x != y)

    if satisfy(solve=True):
        with open('nqc_{}_{}_{}.sol'.format(n, m, seed), 'w') as file:
            for i in range(n):
                print(''.join(['Q ' if qs[i] == j else '. ' for j in range(n)]), file=file)
            print('', file=file)
        print('Satisfiable ...')
    else:
        with open('nqc_{}_{}_{}.sol'.format(n, m, seed), 'w') as file:
            print('Infeasible ...', file=file)
        print('Unsatisfiable ...')
