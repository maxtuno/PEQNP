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

import peqnp.cnf as cnf


def load_instance(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return int(lines[0]), sorted(map(int, lines[1:]))


if __name__ == '__main__':

    # python3 ssp.py ssp.txt

    t, universe = load_instance(sys.argv[1])

    cnf.begin(t.bit_length(), key='ssp')
    T = cnf.tensor(dimensions=(len(universe)))
    assert sum(T[[i]](0, universe[i]) for i in range(len(universe))) / t == 1
    cnf.end({'T': T})

    if cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
        sub = [universe[i] for i in range(len(universe)) if T.binary[i]]
        print(t, sum(sub), sub)
    else:
        print('Infeasible ...')
