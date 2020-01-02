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

    xs = vector(size=size // 3, bits=size)
    ys = vector(size=size // 3, bits=size)

    all_different(xs)
    all_different(ys)

    apply_dual(xs, lambda a, b: a & b == 0)
    apply_dual(ys, lambda a, b: a & b == 0)

    for x, y in zip(xs, ys):
        assert sum(switch(x, i, neg=True) for i in range(size)) == 2
        assert sum(switch(y, i, neg=True) for i in range(size)) == 1
        assert sum(switch(x, i, neg=True) * triplets[i] for i in range(size)) == sum(switch(y, i, neg=True) * triplets[i] for i in range(size))

    if satisfy(turbo=True, log=True):
        for x, y in zip(xs, ys):
            a, b = [triplets[i] for i in range(size) if x.binary[i]]
            c, = [triplets[i] for i in range(size) if y.binary[i]]
            print('{} == {} + {}'.format(c, a, b))
        print(80 * '-')
    else:
        print('Infeasible ...')
