# coding:UTF-8
import random


class Point_2D(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __str__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "Point_2D(%s, %s)" % (self.x, self.y)

    def d(self, p):
        if self == p:
            return 0.0
        else:
            return round((((self.x - p.x) ** 2 + (self.y - p.y) ** 2) ** 0.5), 4)


# 随机生成点
def rand_node_gen(map_size, node_amount):
    nodes = [Point_2D(random.uniform(0, map_size), random.uniform(
        0, map_size)) for i in range(node_amount)]
    return nodes
