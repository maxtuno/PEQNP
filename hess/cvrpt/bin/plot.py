if __name__ == '__main__':
    from data import data
    import matplotlib.pyplot as plt

    plt.style.use('dark_background')

    plt.figure(figsize=(10, 10))
    loc = 0
    total = 0
    for cluster in data:
        total += len(cluster) - 1
        loc += sum([round(abs(complex(cluster[i - 1][1], cluster[i - 1][2]) - complex(cluster[i][1], cluster[i][2]))) for i in range(len(cluster))])
        print(sum([cluster[i][3] for i in range(len(cluster))]))
        i, x, y, d = map(list, zip(*cluster))
        x += [x[0]]
        y += [y[0]]
        plt.plot(x, y, 'o-')

    plt.title('www.PEQNP.science\n{} : {} / {}'.format(loc, len(data), total))

    plt.savefig('cvrp.png')

    print(total)