"""
Copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science

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

# video:  https://youtu.be/9RZa90ZTu1c

from music21 import *

from peqnp import *


# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':

    size = 47

    engine(10)

    x1 = vector(size=size)
    x2 = vector(size=size)
    x3 = vector(size=size)
    x4 = vector(size=size)
    x5 = vector(size=size)

    y1 = vector(size=size)
    y2 = vector(size=size)
    y3 = vector(size=size)
    y4 = vector(size=size)
    y5 = vector(size=size)

    for block in chunks(x1, 11):
        all_different(x1)

    for block in chunks(x2, 7):
        all_different(x2)

    for block in chunks(x3, 5):
        all_different(x3)

    for block in chunks(x4, 3):
        all_different(x4)

    for i in range(size):
        assert 36 <= x1[i] <= 72
        assert 36 <= x2[i] <= 72
        assert 36 <= x3[i] <= 72
        assert 36 <= x4[i] <= 72
        assert 36 <= x4[i] <= 72

        assert 1 <= y1[i] <= 8
        assert 1 <= y2[i] <= 8
        assert 1 <= y3[i] <= 8
        assert 1 <= y4[i] <= 8

        assert 4 <= x1[i] - x2[i]
        assert 4 <= x1[i] - x3[i]
        assert 4 <= x1[i] - x4[i]
        assert 4 <= x2[i] - x3[i]
        assert 4 <= x2[i] - x4[i]
        assert 4 <= x3[i] - x4[i]

    assert sum(y1) == sum(y2) == sum(y3) == sum(y4)

    if satisfy(turbo=True, log=True):
        s = stream.Score(id='mainScore')
        p0 = stream.Part(id='part0')
        p1 = stream.Part(id='part1')
        p2 = stream.Part(id='part2')
        p3 = stream.Part(id='part3')
        p4 = stream.Part(id='part4')

        for i in range(size):
            p0.append(note.Note(pitch=int(x1[i]), quarterLength=int(y1[i]), octave=5))
            p1.append(note.Note(pitch=int(x2[i]), quarterLength=int(y2[i]), octave=4))
            p2.append(note.Note(pitch=int(x3[i]), quarterLength=int(y3[i]), octave=3))
            p3.append(note.Note(pitch=int(x4[i]), quarterLength=int(y4[i]), octave=2))
            p4.append(note.Note(pitch=int(x4[i]), quarterLength=int(y4[i]), octave=1))

        s.insert(0, p0)
        s.insert(0, p1)
        s.insert(0, p2)
        s.insert(0, p3)
        s.insert(0, p4)
        s.show('xml')
    else:
        print('Infeasible ...')
