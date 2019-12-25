"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2019 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////
"""

from peqnp import *


def load_instance(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return int(lines[0]), list(map(int, lines[1:]))


if __name__ == '__main__':

    t, universe = load_instance(sys.argv[1])

    engine(bits=t.bit_length())

    bits, subset = subsets(universe)

    assert sum(subset) == t

    while satisfy(turbo=True):
        solution = [universe[i] for i in range(len(universe)) if bits.binary[i]]
        print(sum(solution), solution)
        print()
