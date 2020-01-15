# Diophantine Equations

### Let be \(x, y \in \mathbb{N}\) solve \(x^3 - x + 1 = y^2\)

```python
from peqnp import *

engine(10)

x = integer()
y = integer()

assert x ** 3 - x + 1 == y ** 2

assert x != 0
assert y != 0

while satisfy(normalize=True):
    print('{0} ** 3 - {0} + 1, {1} ** 2'.format(x, y))
```

```python
5 ** 3 - 5 + 1, 11 ** 2
1 ** 3 - 1 + 1, 1 ** 2
3 ** 3 - 3 + 1, 5 ** 2
```

### Let be \(x, y \in \mathbb{Q}\) solve \(x^3 + xy = y^2\)

```python
from peqnp import *

engine(10)

a = integer()
b = integer()

c = integer()
d = integer()

x = rational(a, b)
y = rational(c, d)

assert x ** 3 + x * y == y ** 2

assert a != 0
assert b != 0

assert c != 0
assert d != 0

while satisfy(normalize=True):
    print('({0} / {1}) ** 3 + ({0} / {1}) * ({2} / {3}), ({2} / {3}) ** 2'.format(a, b, c, d))
```

```python
(6 / 1) ** 3 + (6 / 1) * (18 / 1), (18 / 1) ** 2
(2 / 1) ** 3 + (2 / 1) * (4 / 1), (4 / 1) ** 2
```

### Let be \(x, y \in \mathbb{C}\) solve \(x^3 + x + 1 = y^2\)

```python
from peqnp import *

engine(10)

a = integer()
b = integer()

c = integer()
d = integer()

x = gaussian(a, b)
y = gaussian(c, d)

assert x ** 3 + x + 1 == y ** 2

assert a != 0
assert b != 0

assert c != 0
assert d != 0

while satisfy(normalize=True):
    print('{0} ** 3 + {0} + 1, {1} ** 2'.format(complex(x), complex(y)))
```

```python
(2+1j) ** 3 + (2+1j) + 1, (3+2j) ** 2
```