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


from peqnp import *


def load_file(file_name):
    mat = []
    with open(file_name, 'r') as file:
        for line in file.readlines():
            if line.startswith('p edge '):
                n_ = int(line[len('p edge '):].split(' ')[0])
            elif line.startswith('e '):
                x, y = map(int, line[len('e '):].split(' '))
                mat.append((x, y))
    return n_, mat


if __name__ == '__main__':

    n, matrix = load_file(sys.argv[1])

    size = 3
    while True:

        engine(bits=size.bit_length())

        bits = integer(bits=n)

        assert sum(switch(bits, i) for i in range(n)) == size

        for i in range(n - 1):
            for j in range(i + 1, n):
                if (i, j) not in matrix and (j, i) not in matrix:
                    assert switch(bits, i) + switch(bits, j) <= 1

        if satisfy(turbo=True):
            print(size)
            print(' '.join([str(i) for i in range(n) if not bits.binary[i]]))
            size += 1
        else:
            break
