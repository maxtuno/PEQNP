"""
copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science
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
"""

import random

def list_3sort(lst):
    """
    The 3Sort Algorithm

    Type.                : Sorting Algorithm
    Time Complexity      : O(floor(n^2/4))
    Spatial Complexity   : O(1)
    Author               : Oscar Riveros from www.peqnp.science
    """
    c = 0
    n = len(lst)
    for i in range(n // 2):
        for j in range(i + 1, n - i - 1):
            c += 1
            aux = lst[j]
            if lst[i] > aux:
                lst[j] = lst[i]
                lst[i] = aux    
            aux = lst[n - 1 - j]
            if lst[n - 1 - i] < aux:
                lst[n - 1 - j] = lst[n - 1 - i]
                lst[n - 1 - i] = aux

    aux = lst[n // 2]
    if aux < lst[n // 2 - 1]:
        lst[n // 2] = lst[n // 2 - 1]
        lst[n // 2 - 1] = aux

    return lst, c

if __name__ == '__main__':
    
    b = 32

    for n in range(1, 1000):

        data = [random.randint(1, 2 ** b) for n in range(n)]
        lst, c = list_3sort(data.copy())        
        if sorted(data) == lst:
            print('OK! - Complexity {}'.format(c))
        else:
            raise Exception('ERROR!')
