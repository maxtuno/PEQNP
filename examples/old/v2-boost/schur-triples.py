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

import time
import random
import matplotlib.pyplot as plt
from peqnp import *

if __name__ == '__main__':

    for boost in [True, False]:

        ini = time.time()
        times = []
        sizes = []

        random.seed(0)

        for n in range(1, 12):

            size = 3 * n
            bits = size.bit_length()

            triplets = []
            while len(triplets) < size:
                a = random.randint(1, 2 ** bits)
                b = random.randint(1, 2 ** bits)
                if a != b and a not in triplets and b not in triplets and a + b not in triplets:
                    triplets += [a, b, a + b]
            triplets.sort()
            print(triplets)
            print()

            engine(bits=max(triplets).bit_length() + 1)

            xs, ys = permutations(triplets, size)

            for i in range(0, size, 3):
                assert ys[i] + ys[i + 1] == ys[i + 2]

            if satisfy(turbo=True, boost=boost):
                for i in range(0, size, 3):
                    print('{} == {} + {}'.format(ys[i + 2], ys[i], ys[i + 1]))
            else:
                raise Exception('ERROR! - Increase the bits for engine...')

            times.append(time.time() - ini)
            sizes.append(n)

        plt.plot(sizes, times, 'k-')
        plt.plot(sizes, times, 'r.')
        plt.title('{}'.format('BOOST' if boost else 'no-BOOST'))
        plt.savefig('schur-triples_{}.png'.format('boost' if boost else 'no-boost'))
        plt.close()