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

from peqnp import *


def load_instance(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return int(lines[0]), list(map(int, lines[1:]))


if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Solve the Sum Subset Problem')
        print('Usage   : python3 ssp.py <instance>')
        print('Example : python3 ssp.py data.txt')
        print('Extreme : python3 ssp.py pub.txt (take long time but solve)')
        exit(0)

    t, universe = load_instance(sys.argv[1])

    engine(bits=t.bit_length())

    bits, subset = subsets(universe)

    assert sum(subset) == t

    if satisfy(turbo=True):
        solution = [universe[i] for i in range(len(universe)) if bits.binary[i]]
        print(sum(solution), solution)
        print()
    else:
        print('Infeasible ...')
