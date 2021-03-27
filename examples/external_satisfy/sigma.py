import peqnp as pn

pn.engine(16)

x = pn.integer(key='x')
n = pn.integer(key='n')

pn.sigma(lambda k: k ** 2, 1, n) == x

while pn.external_satisfy(key='sigma', solver='java -jar -Xmx4g blue.jar'):
    print(x, n, sum(k ** 2 for k in range(1, n.value + 1)))
