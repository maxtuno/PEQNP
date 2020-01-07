from peqnp import *

if __name__ == '__main__':

    engine(10)

    y = integer()
    x = integer()

    assert x + -y == 10

    while satisfy():
        print(x + -y)

    ################################################################################
    print(80 * '-')

    engine(10)

    y = integer()
    x = integer()

    assert x + -y == 10

    while satisfy(normalize=True):
        print(x + -y)

    ################################################################################
    print(80 * '-')

    engine(10)

    y = integer()
    x = integer()

    assert x * -y == 10

    while satisfy():
        print(x * -y)

    ################################################################################
    print(80 * '-')

    engine(10)

    y = integer()
    x = integer()

    assert x * -y == 10

    while satisfy(normalize=True):
        print(x * -y)
