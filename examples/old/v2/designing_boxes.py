from matplotlib import pyplot as plt

from peqnp import *

"""
A firm must design a box of minimum dimensions to pack three circular objects
with the following radii: R1 = 6, R2 = 12, and R3 = 16 cm, as shown in Fig. 3.2.
By bearing in mind that the circles placed inside the box cannot overlap,
consider a non-linear programming model that minimises the perimeter of the box.

From: Operation Research Statements and Solutions p-108-107
"""

if __name__ == '__main__':

    opt = 500
    while True:

        engine(16)

        a, b = vector(size=2)
        x1, y1 = vector(size=2)
        x2, y2 = vector(size=2)
        x3, y3 = vector(size=2)

        apply_single([x1, y1], lambda x: x >= 6)
        apply_single([x2, y2], lambda x: x >= 12)
        apply_single([x3, y3], lambda x: x >= 16)

        assert x1 + 6 <= b
        assert y1 + 6 <= a

        assert x2 + 12 <= b
        assert y2 + 12 <= a

        assert x3 + 16 <= b
        assert y3 + 16 <= a

        assert (x1 - x2) ** 2 + (y1 - y2) ** 2 >= (6 + 12) ** 2
        assert (x1 - x3) ** 2 + (y1 - y3) ** 2 >= (6 + 16) ** 2
        assert (x2 - x3) ** 2 + (y2 - y3) ** 2 >= (12 + 16) ** 2

        assert 2 * (a + b) < opt

        if satisfy(turbo=True):
            opt = 2 * (a.value + b.value)
            print('{} = {} x {} | ({}, {}) , ({}, {}) , ({}, {})'.format(opt, a, b, x1, y1, x2, y2, x3, y3))

            circle1 = plt.Circle((x1.value, y1.value), 6, color='r')
            circle2 = plt.Circle((x2.value, y2.value), 12, color='blue')
            circle3 = plt.Circle((x3.value, y3.value), 16, color='g')
            rectangle = plt.Rectangle((0, 0), b.value, a.value, fill=False)

            ax = plt.gca()
            ax.add_patch(circle1)
            ax.add_patch(circle2)
            ax.add_patch(circle3)
            ax.add_patch(rectangle)
            plt.axis('scaled')
            plt.savefig('designing_boxes.png')
            plt.close()

        else:
            break
