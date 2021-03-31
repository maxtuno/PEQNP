import numpy as np
import peqnp as pn

pn.engine(10)

x = pn.integer()
y = pn.integer()

assert pn.rotate(x, -1) == y

while pn.satisfy():
    print(np.vectorize(int)(x.binary))
    print(np.vectorize(int)(y.binary))
    print()

print(80 * '-')

import numpy as np
import peqnp as pn

pn.engine(10)

x = pn.integer()
y = pn.integer()

assert pn.rotate(x, 1) == y

while pn.satisfy():
    print(np.vectorize(int)(x.binary))
    print(np.vectorize(int)(y.binary))
    print()