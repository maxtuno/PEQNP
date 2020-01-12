import sys
from peqnp import *

if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('List all Gaussian Factors of a number.')
        print('Usage   : python3 gaussian_factorizations.py <number>')
        print('Example : python3 gaussian_factorizations.py 3007')
        exit(0)

    rsa = int(sys.argv[1])

    engine(2 * rsa.bit_length())

    x = integer()
    y = integer()

    u = gaussian(x, y)

    z = integer()
    w = integer()

    v = gaussian(z, w)

    assert u * v == gaussian(rsa, rsa)

    while satisfy(normalize=True):
        print(complex(u), complex(v), complex(u) * complex(v))