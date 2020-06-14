import peqnp.cnf as cnf

rsa = 3007

cnf.begin(rsa.bit_length(), key='factorization')
p = cnf.integer()
q = cnf.integer()
assert p * q == rsa
cnf.end({'p': p, 'q': q})

while cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
    print(p, q)