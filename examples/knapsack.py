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
from peqnp import *

if __name__ == '__main__':
    b = int(sys.argv[1])
    n = int(sys.argv[2])

    costs = [random.randrange(1, 2 ** b) for _ in range(n)]
    profits = [random.randrange(1, 2 ** b) for _ in range(n)]
    capacity = sum(random.sample(costs, k=n//2))

    print('n = {};'.format(n))
    print('size = {};'.format(costs))
    print('profit = {};'.format(profits))
    print('capacity = {};'.format(capacity))

    print(80 * '-')

    p = 0

    while True:

        engine(max(sum(costs), sum(profits)).bit_length())

        sc, sub_c = subsets(costs)
        sp, sub_p = subsets(profits)

        assert sum(sub_c) <= capacity
        assert sum(sub_p) > p
        assert sc == sp

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
