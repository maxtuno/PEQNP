"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2019 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////
"""

import random
import sys

from peqnp import *

# ref: https://cstheory.stackexchange.com/questions/16253/list-of-strongly-np-hard-problems-with-numerical-data
if __name__ == '__main__':
    bits = int(sys.argv[1])
    size = 3 * int(sys.argv[2])

    triplets = []
    while len(triplets) < size:
        a = random.randint(1, 2 ** bits)
        b = random.randint(1, 2 ** bits)
        if a != b and a not in triplets and b not in triplets and a + b not in triplets:
            triplets += [a, b, a + b]
    triplets.sort()
    print(triplets)
    print()

    engine(bits=max(triplets).bit_length())

    xs, ys = permutations(triplets, size)

    for i in range(0, size, 3):
        assert ys[i] + ys[i + 1] == ys[i + 2]

    if satisfy(turbo=True, log=True):
        for i in range(0, size, 3):
            print('{} == {} + {}'.format(ys[i + 2], ys[i], ys[i + 1]))
    else:
        print('Infeasible ...')
