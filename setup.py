import sys
from distutils.core import setup, Extension

ext_modules = [
    Extension("slime",
              language="c++",
              sources=['src/SLIME.cc', 'src/SimpSolver.cc', 'src/Solver.cc'],
              include_dirs=['.', 'include'],
              extra_compile_args=['-std=c++98'],
              ),
]
if 'pixie' in sys.argv:
    ext_modules.append(Extension("pixie",
                                 language="c++",
                                 sources=['src/pixie.cc'],
                                 include_dirs=['.', 'include'],
                                 extra_compile_args=['-std=c++17'],
                                 ),)
    sys.argv.remove('pixie')
setup(
    name='PEQNP',
    version='1.1.1',
    packages=['peqnp'],
    url='http://www.peqnp.science',
    license='copyright (c) 2012-2020 Oscar Riveros. All rights reserved.',
    author='Oscar Riveros',
    author_email='contact@peqnp.science',
    description='A Multi Paradigm Constrain Satisfaction Solver.',
    ext_modules=ext_modules,
)
