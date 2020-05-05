# Diophantine

# Let be \(x, y \in \mathbb{N}\) sl \(x^3 - x + 1 = y^2\)

```python
import peqnp as pn

pn.engine(10)

x = pn.integer()
y = pn.integer()

assert x ** 3 - x + 1 == y ** 2

assert x != 0
assert y != 0

while pn.satisfy():
    print('{0} ** 3 - {0} + 1, {1} ** 2'.format(x, y))
```

```python
1 ** 3 - 1 + 1, 1 ** 2
5 ** 3 - 5 + 1, 11 ** 2
3 ** 3 - 3 + 1, 5 ** 2
```

# Let be \(x, y \in \mathbb{Q}\) sl \(x^3 + xy = y^2\)

```python
import peqnp as pn

pn.engine(10)

x = pn.rational()
y = pn.rational()

assert x ** 3 + x * y == y ** 2

while pn.satisfy():
    print('{0} ** 3 + {0} * {1}, {1} ** 2'.format(x, y))
```

```python
(0 / 1) ** 3 + (0 / 1) * (0 / 1), (0 / 1) ** 2
(0 / 2) ** 3 + (0 / 2) * (0 / 16), (0 / 16) ** 2
(6 / 1) ** 3 + (6 / 1) * (18 / 1), (18 / 1) ** 2
(2 / 1) ** 3 + (2 / 1) * (4 / 1), (4 / 1) ** 2
```

# Let be \(x, y \in \mathbb{C}\) sl \(x^3 + x + 1 = y^2\)

```python
import peqnp as pn

pn.engine(10)

x = pn.gaussian()
y = pn.gaussian()

assert x ** 3 + x + 1 == y ** 2

while pn.satisfy():
    print('{0} ** 3 + {0} + 1, {1} ** 2'.format(complex(x), complex(y)))
```

```python
(2 + 1j) ** 3 + (2 + 1j) + 1, (3 + 2j) ** 2
0j ** 3 + 0j + 1, (1 + 0j) ** 2
```

# Vectors

```python
import peqnp as pn

pn.engine(10)

x = pn.vector(size=2, is_gaussian=True)
y = pn.gaussian()

assert sum(x) ** 3 == y ** 5
assert y != complex(0, 0)

while pn.satisfy():
    print('sum({0}) ** 3 == {1} ** 5'.format(x, y))
```

```
sum([(0 + 0j), (1 + 0j)]) ** 3 == (1 + 0j) ** 5
sum([(1 + 0j), (0 + 0j)]) ** 3 == (1 + 0j) ** 5
```

```python
import matplotlib.pyplot as plt
import peqnp as pn

if __name__ == '__main__':
    dim = 2

    pn.engine(10)

    ps = pn.vector(size=dim, is_rational=True)

    assert sum([p ** dim for p in ps]) <= 1

    dots = []
    while pn.satisfy():
        dots.append(list(map(float, ps)))

    x, y = zip(*dots)
    plt.axis('equal')
    plt.plot(x, y, 'r.')
    plt.savefig('rationals.png')
```


