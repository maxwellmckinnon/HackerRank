#!/bin/python3

import sys

global propdict
propdict = {}  # global maps id to (depth, number of subnodes including itself)

class Node:
    def __init__(self, id):
        self.id = id
        self.children = []
        self.parent = None

    def setpNode(self, parentNode):
        self.parent = parentNode

    def addcNode(self, childNode):
        # print("adding child to:", self.id, "child:", childNode.id)
        self.children.append(childNode)

    def childrenids(self):
        l = []
        for c in self.children:
            l.append(c.id)
        return l


def subnodes(node, depth):
    # recursively figure out number of subnodes (including itself)
    # Intended to be called with head node with depth=0 to fill propdict
    global propdict
    print("inner propdict at node id:", node.id, propdict)
    print("node.childrenids:", node.childrenids())

    if not node.children:
        propdict[node.id] = (depth, 1)
        return 1  # base case
    else:
        sum = 1  # 1 to include the current node
        for child in node.children:
            # print("Node, Children:", node.id, node.childrenids())
            sum += subnodes(child, depth + 1)
        propdict[node.id] = (depth, sum)
        return sum


if __name__ == "__main__":
    n = int(input().strip())
    nodelist = []
    nodedict = {}  # map id num to Node
    for a0 in range(n - 1):
        x, y = input().strip().split(' ')
        x, y = [int(x), int(y)]

        # Write Your Code Here

        # flip the order if x is bigger than y because duct tape is instant fix
        if x > y:
            t = y
            y = x
            x = t

        if x == 1:
            print("x1, y", y)
        if x == 449:
            print("x449, y", y)
        if x == 485:
            print("x485, y", y)
        if x == 2:
            print("x2, y", y)
        if x == 46:
            print("x46, y", y)
        if x not in nodedict:
            currentNode = Node(x)
            nodedict[x] = currentNode
        else:
            currentNode = nodedict[x]

        if y not in nodedict:
            childNode = Node(y)
            nodedict[y] = childNode
        else:
            childNode = nodedict[y]

        currentNode.addcNode(childNode)
        childNode.setpNode(currentNode)

        if x == 1:
            Head = currentNode

    # Do work
    # Find depths of all the nodes, find total number of nodes
    # Find total number of nodes under each node
    # Calculate probability / exp value from the depths
    expvalsum = 0
    weightedcount = 0  # count of nodes that is also weighted
    total_nodes = subnodes(Head, 0)
    # print("propdict", propdict)
    # print("nodedict", nodedict)

    # propdict : (depth, subsum of nodes)
    dictkeys = []
    childnodekeys = []
    for o in nodedict:
        dictkeys.append(nodedict[o].id)
        for child in nodedict[o].children:
            childnodekeys.append(child.id)

    # print(dictkeys)
    # print("sorted:", sorted(dictkeys)) # dictkeys looks good, problem with propdict then
    # print(sorted(childnodekeys)) # childnode keys look good
    # print("len chidnodekeys", len(childnodekeys)) # is 499 so good here
    print("propdict:", propdict)
    for id in nodedict.keys():
        if id == 1:
            continue
        remaining_nodes = total_nodes - propdict[id][1]
        expvalsum += propdict[id][0] * remaining_nodes
        weightedcount += propdict[id][0]

    print(expvalsum / weightedcount)