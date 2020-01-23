# Diophantine

### Let be \(x, y \in \mathbb{N}\) sl \(x^3 - x + 1 = y^2\)

```python
from peqnp import *

engine(10)

x = integer()
y = integer()

assert x ** 3 - x + 1 == y ** 2

assert x != 0
assert y != 0

while satisfy():
    print('{0} ** 3 - {0} + 1, {1} ** 2'.format(x, y))
```

```python
5 ** 3 - 5 + 1, 11 ** 2
1 ** 3 - 1 + 1, 1 ** 2
3 ** 3 - 3 + 1, 5 ** 2
```

### Let be \(x, y \in \mathbb{Q}\) sl \(x^3 + xy = y^2\)

```python
from peqnp import *

engine(10)

x = rational()
y = rational()

assert x ** 3 + x * y == y ** 2

while satisfy():
    print('{0} ** 3 + {0} * {1}, {1} ** 2'.format(x, y))
```

```python
(0 / 1) ** 3 + (0 / 1) * (0 / 1), (0 / 1) ** 2
(0 / 2) ** 3 + (0 / 2) * (0 / 16), (0 / 16) ** 2
(2 / 1) ** 3 + (2 / 1) * (4 / 1), (4 / 1) ** 2
(6 / 1) ** 3 + (6 / 1) * (18 / 1), (18 / 1) ** 2
```

### Let be \(x, y \in \mathbb{C}\) sl \(x^3 + x + 1 = y^2\)

```python
from peqnp import *

engine(10)

x = gaussian()
y = gaussian()

assert x ** 3 + x + 1 == y ** 2

while satisfy():
    print('{0} ** 3 + {0} + 1, {1} ** 2'.format(complex(x), complex(y)))
```

```python
(2+1j) ** 3 + (2+1j) + 1, (3+2j) ** 2
0j ** 3 + 0j + 1, (1+0j) ** 2
```

# Vectors

```python
from peqnp import *

engine(10)

x = vector(size=2, is_gaussian=True)
y = gaussian()

assert sum(x) ** 3 == y ** 5
assert y != complex(0, 0)

while satisfy():
    print('sum({0}) ** 3 == {1} ** 5'.format(x, y))

```

```
sum([(0+0j), (1+0j)]) ** 3 == (1+0j) ** 5
sum([(1+0j), (0+0j)]) ** 3 == (1+0j) ** 5
```

```python

import matplotlib.pyplot as plt
from peqnp import *

if __name__ == '__main__':
    dim = 2

    engine(10)

    ps = vector(size=dim, is_rational=True)

    assert sum([p ** dim for p in ps]) <= 1

    dots = []
    while satisfy():
        dots.append(list(map(float, ps)))

    x, y = zip(*dots)
    plt.axis('equal')
    plt.plot(x, y, 'r.')
    plt.savefig('rationals.png')
```
