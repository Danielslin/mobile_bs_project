# coding:UTF-8

from collections import namedtuple
import math

grid = namedtuple('grid', ['x', 'y'])


def manhattan_dis(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


def dis(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) * 10


class AStarNode(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attr = "ground"
        self.parent = None

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __str__(self):
        return "AStarNode(%s,%s)" % (self.x, self.y)

    def __repr__(self):
        return "AStarNode(x=%s, y=%s)" % (self.x, self.y)
