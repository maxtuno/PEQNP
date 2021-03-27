import peqnp as pn

rsa = 3007

pn.engine(rsa.bit_length())

p = pn.integer(key='p')
q = pn.integer(key='q')
assert p * q == rsa

while pn.external_satisfy(key='factorization', solver='java -jar -Xmx4g blue.jar'):
    print(p, q)