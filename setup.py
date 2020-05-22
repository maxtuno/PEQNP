import sys
from distutils.core import setup, Extension

ext_modules = [
    Extension("SLIME",
              language="c++",
              sources=['sdk/solvers/slime/peqnp_sat.cc', 'sdk/solvers/slime/src/Solver.cc'],
              include_dirs=['sdk/sat/', 'sdk/solvers/slime/', 'sdk/solvers/slime/include'],
              extra_compile_args=['-std=c++11'],
              ),
    Extension("PIXIE",
              language="c++",
              sources=['sdk/solvers/pixie/peqnp_mip.cc'],
              include_dirs=['sdk/mip/', 'sdk/solvers/pixie/', 'sdk/solvers/pixie/include'],
              extra_compile_args=['-std=c++11'],
              ),
]
if 'no-solver' in sys.argv:
    del ext_modules[:]
    if 'no-solver' in sys.argv:
        sys.argv.remove('no-solver')
setup(
    name='PEQNP',
    version='2.1.0',
    packages=['peqnp'],
    url='http://www.peqnp.science',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='PEQNP II Mathematical Programming Solver from http://www.peqnp.com',
    ext_modules=ext_modules,
)
