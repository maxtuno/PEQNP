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

if __name__ == '__main__':

    rsa = int(sys.argv[1])

    engine(bits=rsa.bit_length())

    p, q = integer(), integer()

    assert p * q == rsa

    assert 1 < p < q < rsa

    if satisfy(turbo=True):
        print(p, q)
    else:
        print('Is Prime!')
