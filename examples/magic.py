from peqnp import *

n = 3
while True:
  engine((n ** 3).bit_length())

  c = integer()
  xs = matrix(dimensions=(n, n))

  apply_single(flatten(xs), lambda x: x > 0)
  apply_dual(flatten(xs), lambda a, b: a != b)

  for i in range(n):
    assert sum(xs[i][j] for j in range(n)) == c

  for j in range(n):
    assert sum(xs[i][j] for i in range(n)) == c

  assert sum(xs[i][i] for i in range(n)) == c
  assert sum(xs[i][n - 1 - i] for i in range(n)) == c

  if satisfy(turbo=True):
    print(c)
    for i in range(n):
      print(xs[i])
    print()
    n += 1
  else:
    print('Infeasible ...')
    break