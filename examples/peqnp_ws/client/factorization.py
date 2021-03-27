import peqnp as pn

rsa = 3007

pn.engine(rsa.bit_length())

p = pn.integer(key='p')
q = pn.integer(key='q')

assert p * q == rsa

while pn.external_satisfy(key='remote', solver='python3 remote_solver.py'):
    print(p, q)
