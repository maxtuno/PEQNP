from peqnp import *

if __name__ == '__main__':

    engine(4)

    q = integer(key='p')
    p = integer(key='q')

    assert p + q == 1

    if satisfy(solve=True, turbo=True, log=True, assumptions=[], cnf_path='test.cnf'):
        print(p, q)