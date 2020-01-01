from peqnp import *

if __name__ == '__main__':

    engine(10)

    data = [2, 3, 5, 7]

    x = integer()

    index = element(x, data)

    while satisfy():
        print(x, index)