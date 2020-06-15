"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# !pip install PEQNP

# ref: http://www.csc.kth.se/~viggo/wwwcompendium/node152.html

import random

import peqnp as pn

bits = 4
n = 7
m = 5


D = [random.randint(1, 2 ** bits) for _ in range(n * m)]

print('D   : {}'.format(D))

pn.engine(sum(D).bit_length())

b = pn.integer()
seq, val = pn.permutations(D, m * n)

for i in range(m):
    assert sum(val[n*i: n*(i + 1)]) == b

if pn.satisfy(turbo=True):
    print('SEQ : {}'.format(seq))
    print('VAL : {}'.format(val))
    print('b   : {}'.format(b))
    print('')
    for i in range(m):
        print(val[n*i: n*(i + 1)], end=' ')
    print('\n')
else:
    print('Infeasible ...')
