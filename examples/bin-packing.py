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

import math
import sys

from peqnp import *

if __name__ == '__main__':

    # load instance
    elements = []
    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()
        # first line is size
        size = int(lines[0])
        del lines[0]
        # second line is capacity
        capacity = int(lines[0])
        del lines[0]
        # next the "size" elements
        for i in range(size):
            elements.append(int(lines[i]))

    # theoretical optimal distribution possible
    bins = math.ceil(sum(elements) / capacity)
    while True:

        engine(bits=capacity.bit_length())

        # an array of "bins"-size elements and of "len(elements)"-bits
        slots = vector(bits=len(elements), size=bins)

        # only one assignment for element
        for i in range(len(elements)):
            assert sum(switch(slot, i) for slot in slots) == 1

        # all slots satisfy the capacity requirement
        for slot in slots:
            assert sum(switch(slot, i) * elements[i] for i in range(len(elements))) <= capacity

        if satisfy(turbo=True, log=True):
            # save the solution
            print('Solution for {} bins...'.format(bins))
            # the binary location of each element on slots
            print()
            for slot in slots:
                print(''.join(['_' if boolean else '#' for boolean in slot.binary]))
            # the singular location of each element on slots
            print()
            for slot in slots:
                sub = [item for i, item in enumerate(elements) if not slot.binary[i]]
                print(sum(sub), sub)
            # first solution is optimal exit
            break
        else:
            print('No solution for {} bins...'.format(bins))
            # no solution for "bins" bins then try with "bins + 1"
            bins += 1
