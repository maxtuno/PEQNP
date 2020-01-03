from peqnp import *

if __name__ == '__main__':

    # On Diophantine equation x^4 + y^4 = n(u^4 + v^4)
    # https://www.degruyter.com/view/j/ms.2019.69.issue-6/ms-2017-0305/ms-2017-0305.xml

    bits = 32

    engine(bits)

    x, y, u, v, n = integer(), integer(), integer(), integer(), integer()

    apply_single([x, y, u, v, n], lambda k: k > 1)

    assert x ** 4 + y ** 4 == n * (u ** 4 + v ** 4)

    assert x ** 4 + y ** 4 < oo
    assert n * (u ** 4 + v ** 4) < oo

    while satisfy():
        print('{0} ** 4 + {1} ** 4 == {4} * ({2} ** 4 + {3} ** 4)'.format(x, y, u, v, n))
