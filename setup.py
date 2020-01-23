from distutils.core import setup, Extension

setup(
    name='PEQNP',
    version='0.2.3',
    packages=['peqnp'],
    url='http://www.peqnp.science',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='The PEQNP System its a automatic CNF encoder and SAT Solver for General Constrained Diophantine Equations and NP-Complete Problems, full integrated with Python 3.',
    ext_modules=[
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
    ],
)
