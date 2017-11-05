#!/bin/python3

if __name__ == "__main__":
    n = int(input().strip())
    g = {i + 1: [] for i in range(n)}
    for a0 in range(n - 1):
        x, y = input().strip().split(' ')
        x, y = [int(x), int(y)]
        g[x].append(y)
        g[y].append(x)
    d = {0: [1]}
    nodes = set(range(2, n + 1))
    level = 0
    while nodes:
        d[level + 1] = []
        for i in d[level]:
            for j in g[i]:
                if j in nodes:
                    d[level + 1].append(j)
                    nodes.remove(j)
        level += 1

    x = 0
    p = 0
    for i in d:
        di = len(d[i])
        x += di * i
        p += di * i * (i + 1) / 2
    print(n - p / x)