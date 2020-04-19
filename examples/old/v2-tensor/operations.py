import numpy as np
from peqnp import *

if __name__ == '__main__':

    engine(1 * 2 * 3)

    A = tensor(dimensions=[1, 2, 3])
    B = tensor(dimensions=[1, 2, 3])
    C = tensor(dimensions=[1, 2, 3])

    assert A ** B == C
    assert A > 0
    assert B > 0
    assert C > 0

    while satisfy():
        print(A, B, C)
        print()
        print(np.vectorize(int)(A.binary))
        print()
        print(np.vectorize(int)(B.binary))
        print()
        print(np.vectorize(int)(C.binary))
        print(80 * '-')
