import sys
from distutils.core import setup, Extension

ext_modules = [
    Extension("slime",
              language="c++",
              sources=['src/SLIME.cc', 'src/SimpSolver.cc', 'src/Solver.cc'],
              include_dirs=['.', 'include'],
              extra_compile_args=['-std=c++11'],
              ),
    Extension("pixie",
              language="c++",
              sources=['src/pixie.cc'],
              include_dirs=['.', 'include'],
              extra_compile_args=['-std=c++11'],
              ),
]
if 'no-solver' in sys.argv:
    del ext_modules[:]
    if 'no-solver' in sys.argv:
        sys.argv.remove('no-solver')
setup(
    name='PEQNP',
    version='5.1.3',
    packages=['peqnp', 'peqnp.cnf', 'peqnp.sdk'],
    url='http://www.peqnp.com',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='PEQNP Mathematical Solver from http://www.peqnp.com',
    ext_modules=ext_modules,
)
