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

import math
import random
import matplotlib.pyplot as plt
from peqnp import *

if __name__ == '__main__':

    n = 100
    b = 500

    locations = [complex(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    elements = [random.randint(1, b) for _ in range(n)]
    capacity = sum(random.sample(elements, k=n // 4))
    bins = math.ceil(sum(elements) / capacity)
    while True:

        print('BINS : {} - {}'.format(bins, capacity))

        engine(bits=capacity.bit_length())

        X = tensor(dimensions=(n, bins))

        for i in range(n):
            assert sum(X[[i, j]](0, 1) for j in range(bins)) == 1

        for j in range(bins):
            assert sum(X[[i, j]](0, elements[i]) for i in range(n)) <= capacity

        opt = math.inf
        while satisfy():
            cur = 0
            ds = []
            for j in range(bins):
                sub = [item for i, item in enumerate(elements) if X.binary[i][j]]
                loc = [complex(0, 0)] + [locations[i] for i in range(n) if X.binary[i][j]]

                def oracle(seq):
                    return sum(abs(loc[seq[i - 1]] - loc[seq[i]]) for i in range(len(seq)))


                seq = hess_sequence(len(loc), oracle)

                ds.append((sub, loc, seq))

                cur += oracle(seq)

                if cur > opt:
                    break

            if cur < opt:
                opt = cur

                print(80 * '-')
                for sub, loc, seq in ds:

                    print(sum(sub), sub, seq)

                    x, y = zip(*[(loc[i].real, loc[i].imag) for i in seq + [seq[0]]])
                    plt.plot(x, y, 'o-')
                plt.title('OPT : {}'.format(opt))
                plt.savefig('cvrp.png')
                plt.close()

        if opt != math.inf:
            print(80 * '-')
            print('OPTIMUM FOUND ...')
            break
        else:
            bins += 1