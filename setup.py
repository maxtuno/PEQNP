from distutils.core import setup, Extension

setup(
    name='PEQNP',
    version='0.1.40',
    packages=['peqnp'],
    url='http://www.peqnp.science',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='General Constrained Diophantine Equation Solver',
    package_data={'peqnp': ['*.cnf', 'peqnp/*.cnf']},
    ext_modules=[
        Extension("slime",
                  language="c++",
                  sources=['src/SLIME.cc', 'src/SimpSolver.cc', 'src/Solver.cc'],
                  include_dirs=['.', 'include'],
                  extra_compile_args=['-std=c++98'],
                  ),
    ],
)
