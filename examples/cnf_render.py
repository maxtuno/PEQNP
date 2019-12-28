from peqnp import *

if __name__ == '__main__':

    engine(2)

    x = integer(key='x')
    y = integer(key='y')

    assert x <= 10
    assert y <= 10

    assert x * y == 6

    if satisfy(solve=False, turbo=True, log=True, assumptions=[-1], cnf_path='test.cnf'):
        print(x)