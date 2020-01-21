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

# video : https://github.com/maxtuno/PEQNP

import random
from tkinter import *

from peqnp import *


class Ball:
    def __init__(self, idx):
        self.idx = idx
        self.shape = canvas.create_oval(0, 0, SIZE, SIZE, fill='red')
        self.speed_x = random.randint(1, 10)
        self.speed_y = random.randint(1, 10)
        self.active = True
        self.move_active()

    def ball_update(self):
        canvas.move(self.shape, self.speed_x, self.speed_y)
        pos = canvas.coords(self.shape)
        if pos[2] >= WIDTH or pos[0] <= 0:
            self.speed_x *= -1
        if pos[3] >= HEIGHT or pos[1] <= 0:
            self.speed_y *= -1

    def move_active(self):
        if self.active:
            self.ball_update()
            tk.after(10, self.move_active)

    @property
    def position(self):
        pos = canvas.coords(self.shape)
        return complex(pos[2] - SIZE // 2, pos[3] - SIZE // 2)


def distance(seq):
    return sum(abs(balls[seq[i - 1]].position - balls[seq[i]].position) for i in range(len(balls)))


def update():
    seq = hess_sequence(len(balls), oracle=distance)
    canvas.delete('lines')
    for i in range(len(seq)):
        x = balls[seq[i - 1]].position.real
        y = balls[seq[i - 1]].position.imag
        z = balls[seq[i]].position.real
        w = balls[seq[i]].position.imag
        canvas.create_line(x, y, z, w, fill="white", tags='lines')
    tk.after(10, update)


if __name__ == '__main__':
    WIDTH = 640
    HEIGHT = 480
    SIZE = 30
    N = 10

    tk = Tk()
    tk.title('PEQNP - Realtime TSP with HESS')
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    balls = []

    for i in range(N):
        balls.append(Ball(i))

    tk.after(10, update)

    tk.mainloop()
