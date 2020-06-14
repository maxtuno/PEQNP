# PEQN CNF Submodule Examples

A pure CNF encoder functionality, you can use with any solver that support the standard output of SAT Races, for online use with Jupyter Notebooks use the standard mode http://www.peqnp.com.


##### Note: To install PEQNP without builtin solvers to use with pre-build solvers that implement PEQNP_API or use with pure CNF submodule install with:
    
    pip install PEQNP --install-option=no-solver --upgrade 
     
##### Note: Performance depend on SAT Solver, try any solver from http://www.satcompetition.org  

# Main Differences

    import peqnp.cnf as cnf
    
    cnf.begin(bits=7, key='my_problem')
    x = cnf.integer()
    _2 = cnf.constant(2)
    assert 2 ** x == 128
    cnf.end({'x': x}) # for vector see multiset_reconstruction_by_differences.py
    while cnf.satisfy(solver='path_to_my_sat_race_sat_solver', params='some params to solver'):
        peinr(x) 

# BLUE
 A Powerful and Portable SAT Solver for Java https://github.com/maxtuno/blue
 
 very simple:
 
 java -jar -Xmx4g blue.jar file.cnf
 
Blue is based on Minisat many thanks to Niklas Een, Niklas Sorensson for this great solver.

MIT License

Copyright (c) 2019 Oscar Riveros [oscar.riveros@peqnp.science]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
