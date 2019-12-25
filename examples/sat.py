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


def load_data(file_name):
    n_, m_, cnf_ = 0, 0, []
    with open(file_name, 'r') as cnf_file:
        lines = cnf_file.readlines()
        for line in filter(lambda x: not x.startswith('c'), lines):
            if line.startswith('p cnf'):
                n_, m_ = list(map(int, line[6:].split(' ')))
            else:
                cnf_.append(list(map(int, line.rstrip('\n')[:-2].split(' '))))
    return n_, m_, cnf_


if __name__ == '__main__':

    n, m, cnf = load_data(sys.argv[1])

    engine(bits=2)

    x = integer(bits=n)

    for cls in cnf:
        assert functools.reduce(operator.ior, (switch(x, abs(lit) - 1, neg=lit > 0) for lit in cls)) != 0

    if satisfy(turbo=True):
        print('SAT')
        print(' '.join(map(str, [(i + 1) if b else -(i + 1) for i, b in enumerate(x.binary)])) + ' 0')
    else:
        print('UNSAT')
