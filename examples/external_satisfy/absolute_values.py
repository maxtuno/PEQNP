import peqnp as pn

pn.engine(4)

x = pn.integer(key='x')
y = pn.integer(key='y')

assert abs(x - y) == 1

while pn.external_satisfy(key='absolute_values', solver='java -jar -Xmx4g blue.jar'):
    print(x, y, x - y, abs(x - y))