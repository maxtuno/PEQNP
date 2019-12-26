import setuptools
from distutils.core import setup, Extension

setup(
    name='PEQNP',
    version='0.1.0',
    packages=['peqnp'],
    url='https://github.com/maxtuno/PEQNP',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='General Constrained Diophantine Equation Solver',
    python_requires='>=3.6',
    package_data={'': ['README.txt', 'LICENCE.txt', 'pytransform/*']},
    ext_modules=[
        Extension("slime",
                  sources=['src/SLIME.cc' ,'src/SimpSolver.cc' ,'src/Solver.cc'],
                  include_dirs=['.', 'include'],
                  extra_compile_args=['-std=c++98', '-Os', '-mtune=generic', '-DNEDEBUG', '-g0', '-Wno-reorder', '-Wno-unused-value'],
                  ),
    ],
)
