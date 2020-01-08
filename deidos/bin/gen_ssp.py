if __name__ == '__main__':

    import sys
    import random

    d = int(sys.argv[1])
    n = int(sys.argv[2])

    # random.seed(int(sys.argv[3]))

    universe = sorted([random.randrange(1, 2 ** d) for i in range(n)], reverse=True)

    # random.seed(int(sys.argv[4]))

    t = sum(random.sample(universe, k=n // 2))

    with open('data.txt', 'w') as data:
        data.write('{}\n{}'.format(len(universe), t))
        for o in universe:
            data.write('\n{}'.format(o))