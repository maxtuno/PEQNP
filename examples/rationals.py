from peqnp import *

if __name__ == '__main__':

    engine(10)

    a = integer()
    b = integer()

    c = integer()
    d = integer()

    x = gaussian(a, b)
    y = gaussian(c, d)

    assert x ** 3 - x - 1 == y ** 2

    while satisfy(normalize=True):
        print('({0} / {1}) ** 3 - ({0} / {1}) - 1, ({2} / {3}) ** 2'.format(a, b, c, d))