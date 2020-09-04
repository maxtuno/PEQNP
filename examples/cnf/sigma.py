import peqnp.cnf as cnf

cnf.begin(16, key='sigma')

x = cnf.integer()
n = cnf.integer()

cnf.sigma(lambda k: k ** 2, 1, n) == x

cnf.end({'x':x, 'n':n})

while cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
    print(x, n, sum(k ** 2 for k in range(1, n.value + 1)))
