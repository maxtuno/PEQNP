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

bits = 10
n = 20
m = 5


D = [random.randint(1, 2 ** bits) for _ in range(n * m)]

print('D   : {}'.format(D))

pn.engine(sum(D).bit_length())

b = pn.integer()
seq, val = pn.permutations(D, m * n)

for i in range(m - 1):
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

"""
D   : [64257, 26406, 49364, 44750, 52303, 26128, 23041, 61294, 34167, 42202, 15269, 19118, 6948, 48134, 8028, 6182, 31002, 23212, 48060, 40068, 33792, 31127, 10725, 52812, 3225, 3968, 42633, 18464, 2805, 2107, 30270, 62708, 21774, 33366, 29457, 29435, 44821, 53098, 33065, 28215, 60794, 31495, 27955, 61211, 28704, 52792, 50206, 31553, 25389, 4848]
SEQ : [34, 49, 5, 38, 18, 37, 28, 11, 36, 48, 30, 26, 32, 33, 39, 15, 1, 43, 44, 14, 19, 9, 47, 17, 46, 27, 29, 16, 3, 24, 6, 45, 40, 21, 20, 12, 8, 25, 35, 22, 13, 2, 23, 7, 42, 41, 31, 10, 4, 0]
VAL : [29457, 4848, 26128, 33065, 48060, 53098, 2805, 19118, 44821, 25389, 30270, 42633, 21774, 33366, 28215, 6182, 26406, 61211, 28704, 8028, 40068, 42202, 31553, 23212, 50206, 18464, 2107, 31002, 44750, 3225, 23041, 52792, 60794, 31127, 33792, 6948, 34167, 3968, 29435, 10725, 48134, 49364, 52812, 61294, 27955, 31495, 62708, 15269, 52303, 64257]
b   : 286789

[29457, 4848, 26128, 33065, 48060, 53098, 2805, 19118, 44821, 25389] [30270, 42633, 21774, 33366, 28215, 6182, 26406, 61211, 28704, 8028] [40068, 42202, 31553, 23212, 50206, 18464, 2107, 31002, 44750, 3225] [23041, 52792, 60794, 31127, 33792, 6948, 34167, 3968, 29435, 10725] [48134, 49364, 52812, 61294, 27955, 31495, 62708, 15269, 52303, 64257] 
"""