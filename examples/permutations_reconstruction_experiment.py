import random
import time

import matplotlib.pyplot as plt
from peqnp import *


# Permutation Reconstruction fromDifferences
# from https://arxiv.org/pdf/1410.6396.pdf
def gen_instance(n):
    y = list(range(1, n + 1))
    random.shuffle(y)
    return [abs(y[i + 1] - y[i]) for i in range(n - 1)]


if __name__ == '__main__':
    sizes, times = [], []
    n = 1
    while True:
        n += 1
        print('size : {}'.format(n))
        # Generate the problem
        diffs = gen_instance(n)
        # initialize the process
        ini = time.time()
        # Because the largest number on the problem (with operations) is bits of n there is the necessarily bits for the engine and add 1 for the subtraction.
        engine(n.bit_length() + 1)
        # Declare a n-vector of integer variables to store the solution.
        x = vector(size=n)
        # All elements are different and from 1 to n there is a permutation.
        all_different(x)
        apply_single(x, lambda a: 1 <= a <= n)
        # The i-th element of the instance is the absolute difference of two consecutive elements
        for i in range(n - 1):
            assert index(i, diffs) == one_of([x[i + 1] - x[i], x[i] - x[i + 1]])
        # Solve the problem for only one solution, according to the paper are two equivalents.
        if satisfy(turbo=True):
            end = time.time() - ini
            xx = [abs(x[i + 1] - x[i]) for i in range(n - 1)]
            if xx == diffs:
                print(x)
                print(xx)
                print('OK! - {}s'.format(end))
                sizes.append(n)
                times.append(end)
                plt.clf()
                plt.figure(figsize=(10, 10))
                plt.title('Permutations Reconstruction by Differences Size vs Time with PEQNP')
                plt.plot(sizes, times, 'o-')
                plt.savefig('permutations_reconstruction.png')
                plt.close()
            else:
                raise Exception('Error!')
        else:
            raise Exception('Error!')