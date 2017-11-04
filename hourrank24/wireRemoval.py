#!/bin/python3

import sys
import copy

nd = {}  # id: [list of ids]
traveled = {1}  # set of ids traveled to already

# TO sum up individual pieces
# The end will take EV / weighted_total for the answer
weighted_total = 0  # add the depths all up
EV = 0  # Add the (depth * nodes_remain) all up


def nodes_under(n=1, depth=0):
    # recursively expand upon id = n, intended to be called on head n == 1, depth == 1 the first time around
    global EV
    global weighted_total
    global traveled
    global nd
    total_nodes = len(nd)

    downward_children = []
    for id in nd[n]:
        if id not in traveled:
            downward_children.append(id)
            traveled.add(id)
    # print("downard children of id {}: {}".format(n, downward_children))
    if len(downward_children) == 0:
        # print("Adding contribution from node id:", n)
        # print("EV:{}, weighted_total:{}".format(depth * (total_nodes - 1), depth))
        EV += depth * (total_nodes - 1)
        weighted_total += depth
        return 1

    subnodescnt = 1
    for id in downward_children:
        subnodescnt += nodes_under(n=id, depth=depth + 1)
    # print("n and its children:", n, downward_children)
    # print("node count under n:", n, subnodescnt)
    # print("nodes remaining after cutting {}: {}".format(n, total_nodes - (subnodescnt)))
    EV += depth * (total_nodes - (subnodescnt))
    weighted_total += depth
    return subnodescnt


if __name__ == "__main__":
    n = int(input().strip())
    for a0 in range(n - 1):
        x, y = input().strip().split(' ')
        x, y = [int(x), int(y)]

        # Write Your Code Here
        if x in nd:
            nd[x].append(y)
        else:
            nd[x] = [y]
        if y in nd:
            nd[y].append(x)
        else:
            nd[y] = [x]

    # print(nd)
    nodes_under()
    # print(EV)
    # print(weighted_total)
    print(EV / weighted_total)
    # print(nd)
    # print(traveled)

    # feed first node into recursive algorithm

