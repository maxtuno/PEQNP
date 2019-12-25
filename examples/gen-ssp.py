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

if __name__ == '__main__':
    bits = int(sys.argv[1])
    size = int(sys.argv[2])

    universe = [random.randrange(1, 2 ** bits) for _ in range(size)]
    t = sum(random.sample(universe, k=size // 2))

    print(t)
    for item in universe:
        print(item)
