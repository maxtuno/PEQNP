import sys
import setuptools
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
setup(
    name='PEQNP',
    version='6.1.0',
    packages=['peqnp'],
    url='http://www.peqnp.com',
    license='copyright (c) 2012-2021 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='PEQNP Mathematical Solver from http://www.peqnp.com',
    ext_modules=ext_modules,
)
