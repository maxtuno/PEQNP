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

import pandas as pd
from peqnp import *

"""
NOTE: The data need to be normalized, take it how a working example only.
"""


def np_complete_query(cols, withs, count, size):
    """
    Simple NP-Complete Query Example
    :param cols: Name of the cols, the fist is the IDs (for identification only)
    :param withs: Optimality conditions, for the example <, > (min, max)
    :param count: The total numbers of rows to get
    :param size: The size of the sample set (data base) more data need more ram, take car with this.
    :return: The selected ids
    """
    qs = ds[cols][:size]
    for col in cols[1:]:
        qs[col] = [int(float(val.replace('mcg', '').replace('mg', '')) * 1000) if isinstance(val, str) else val for val in qs[col].values]

    idx, values = [], {}

    down, up = 0, int(sum(sum(qs[cols[1:]].values)))

    max_data_bits = up.bit_length()

    while True:

        engine(max_data_bits)

        # An "size" bits integer, each bit its a row on the table.
        select = integer(bits=size)

        for col, cmd in zip(cols, withs):
            if cmd == '<':
                if col not in values:
                    values[col] = up
                # Minimize the selected column.
                assert sum(switch(select, i, neg=True) * qs[col][i] for i in range(size)) < values[col]

            if cmd == '<=':
                if col not in values:
                    values[col] = up
                # Minimize the selected column.
                assert sum(switch(select, i, neg=True) * qs[col][i] for i in range(size)) <= values[col]

            if cmd == '>':
                if col not in values:
                    values[col] = down
                # Maximize the selected column.
                assert sum(switch(select, i, neg=True) * qs[col][i] for i in range(size)) > values[col]

            if cmd == '>=':
                if col not in values:
                    values[col] = down
                # Maximize the selected column.
                assert sum(switch(select, i, neg=True) * qs[col][i] for i in range(size)) >= values[col]

        # Ensure there is only "count" elements on the result
        assert sum(switch(select, i, neg=True) for i in range(size)) == count

        if satisfy(turbo=True):
            idx = [i for i in range(size) if select.binary[i]]
            print(qs.loc[idx])
            for col in cols[1:]:
                values[col] = sum(qs[col][i] for i in range(size) if select.binary[i])
            print(values)
            print()
        else:
            return idx


if __name__ == '__main__':
    # https://www.kaggle.com/trolukovich/nutritional-values-for-common-foods-and-products
    ds = pd.read_csv('nutrition.csv')

    # SELECT IDs FROM TOP(100) NUTRITION
    # WHERE
    # sum(CALORIES) is MINIMAL AND
    # sum(CHOLESTEROL) is MINIMAL AND
    # -- This is the mandatory column
    # sum(VITAMIN_B12) IS MAXIMAL* AND
    # count(IDs) == 10
    ids = np_complete_query(['name', 'calories', 'vitamin_b12', 'cholesterol'], ['', '<=', '>=', '<'], count=10, size=100)

    print(ids)

    """
                          name  calories  vitamin_b12  cholesterol
    5         Cauliflower, raw        25            0            0
    9       Vegetarian fillets       290         4200            0
    10     PACE, Picante Sauce        25            0            0
    16  Pie, lemon, fried pies       316           80            0
    25  PACE, Green Taco Sauce        25            0            0
    39  Lentils, raw, sprouted       106            0            0
    72   Emu, raw, flat fillet       102         6120        71000
    80   Broccoli, raw, stalks        28            0            0
    95   Pears, red anjou, raw        62            0            0
    96   Horseradish, prepared        48            0            0
    {'calories': 1027, 'vitamin_b12': 10400, 'cholesterol': 71000}
    
    [5, 9, 10, 16, 25, 39, 72, 80, 95, 96]
    """
