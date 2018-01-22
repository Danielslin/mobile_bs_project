# coding:UTF-8
import random
import math


class Point_2D(object):

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __str__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def d(self, p):
        if self == p:
            return 0.0
        else:
            return round(math.hypot(self.x - p.x, self.y - p.y), 4)


class segment(object):

    def __init__(self, pa, pb):
        self.pa, self.pb = pa, pb
        self.len = pa.d(pb)
        self.k = (pb.y - pa.y) / (pb.x - pa.x)

    def __eq__(self, other):
        return (self.pa, self.pb) == (other.pa, other.pb)

    def __hash__(self):
        return hash(str(self.pa) + ',' + str(self.pb))

    def __str__(self):
        return "Segment(%s, %s)" % (self.pa, self.pb)

    def __repr__(self):
        return "Segment(%s, %s)" % (self.pa, self.pb)

    def minX(self):
        return min(self.pa.x, self.pb.x)

    def maxX(self):
        return max(self.pa.x, self.pb.x)

    def minY(self):
        return min(self.pa.y, self.pb.y)

    def maxY(self):
        return max(self.pa.y, self.pb.y)


# 随机生成点
def RandomNode(map_size):
    newPoint = Point_2D(random.uniform(0, map_size), random.uniform(0, map_size))
    return newPoint


# 批量随机生成点
def RandomNodeGeneration(map_size, node_amount):
    nodes = [RandomNode(map_size) for i in range(node_amount)]
    return nodes
