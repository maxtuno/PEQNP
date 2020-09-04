import peqnp.cnf as cnf

cnf.begin(4, key='absolute_values')

x = cnf.integer()
y = cnf.integer()

assert abs(x - y) == 1

cnf.end({'x':x, 'y':y})

while cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
    print(x, y, x - y, abs(x - y))