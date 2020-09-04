import peqnp.sdk as cnf

cnf.engine(4, sat_solver_path='lib/libSLIME.dylib', mip_solver_path='lib/libLP_SOLVE.dylib', info=True)

x = cnf.integer()
y = cnf.integer()

assert abs(x - y) == 1

while cnf.satisfy():
    print(x, y, x - y, abs(x - y))