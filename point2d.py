# coding:UTF-8
import random
import math


class Point_2D(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def __mul__(self, num):
        return Point_2D(self.x * num, self.y * num)

    def __add__(self, other):
        return Point_2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point_2D(self.x - other.x, self.y - other.y)

    def d(self, p):
        if self == p:
            return 0.0
        else:
            return round(math.hypot(self.x - p.x, self.y - p.y), 4)


class segment(object):

    def __init__(self, pa, pb):
        self.pa, self.pb = pa, pb
        self.len = pa.d(pb)

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

    def midPoint(self):
        return Point_2D(math.fsum([self.pa.x, self.pb.x]) / 2.0, math.fsum([self.pa.y, self.pb.y]) / 2.0)

    def pointInSegment(self, p):
        return (self.pa.x - p.x) * (self.pb.y - p.y) - (
            self.pb.x - p.x) * (self.pa.y - p.y) == 0 and p.x >= self.minX() and p.x <= self.maxX()


# 随机生成点
def RandomNode(map_size):
    newPoint = Point_2D(random.randint(0, map_size),
                        random.randint(0, map_size))
    return newPoint


# 批量随机生成点
def RandomNodeGeneration(map_size, node_amount):
    nodes = [RandomNode(map_size) for i in range(node_amount)]
    return nodes
