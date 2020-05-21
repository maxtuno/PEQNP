import sys
from distutils.core import setup, Extension

ext_modules = [
    Extension("SLIME",
              language="c++",
              sources=['sdk/solvers/slime/peqnp_sat.cc', 'sdk/solvers/slime/src/Solver.cc'],
              include_dirs=['sdk/sat/', 'sdk/solvers/slime/', 'sdk/solvers/slime/include'],
              ),
    Extension("PIXIE",
              language="c++",
              sources=['sdk/solvers/pixie/peqnp_mip.cc'],
              include_dirs=['sdk/mip/', 'sdk/solvers/pixie/', 'sdk/solvers/pixie/include'],
              ),
]
setup(
    name='PEQNP',
    version='2.0.1',
    packages=['peqnp'],
    url='http://www.peqnp.science',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='PEQNP II Mathematical Programming Solver from http://www.peqnp.com',
    ext_modules=ext_modules,
)
