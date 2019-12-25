"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2019 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////
"""

import numpy as np
from peqnp import *

if __name__ == '__main__':

    n = int(sys.argv[1])

    np.random.seed(n)

    matrix = np.random.randint(0, 2, size=(n, n))
    matrix -= np.identity(n, dtype=int) * np.diagonal(matrix)

    print(matrix)

    engine(2 * n.bit_length())

    indexes, elements = permutations((1 - matrix).tolist(), n)

    assert sum(elements) == 0

    while satisfy(turbo=True):
        for i in indexes:
            for j in indexes:
                sys.stdout.write('{} '.format(matrix[i.value][j.value]))
            print()
        print()
