# coding:UTF-8

from collections import namedtuple, defaultdict
import math

grid = namedtuple('grid', ['x', 'y'])


def manhattan_dis(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


def dis(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) * 10


class AStarNode(object):

    def __init__(self, *coo):
        self.x = coo[0]
        self.y = coo[1]
        self.parent = None

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __str__(self):
        return "AStarNode(%s,%s)" % (self.x, self.y)

    def __repr__(self):
        return "AStarNode(x=%s, y=%s)" % (self.x, self.y)

    def neighbors(self, exist_map):
        n = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if x != self.x and y != self.y and exist_map[AStarNode(x, y)] == True:
                    n.append(AStarNode(x, y))
        return n

    def gn(self, start_node):
        return dis(self, start_node)

    def hn(self, end_node):
        return manhattan_dis(self, end_node)

    def fn(self, start, end):
        return self.gn(start) + self.hn(end)


def init_map(x_range, y_range, barrier_list=[]):
    map = defaultdict(bool)
    for i in range(x_range):
        for j in range(y_range):
            if AStarNode(i, j) not in barrier_list:
                map[AStarNode(i, j)] = True
    return map


def print_path(start, end):
    print end
    if start != end:
        print_path(start, end.parent)


def A_star(exist_map, start, end):
    open_list = [start]
    close_list = []
    while (len(open_list)) and (end not in close_list):
        open_list.sort(key=AStarNode.fn(start, end))
        current = open_list[0]
        close_list.append(open_list.pop(0))
        neighbors = current.neighbors(exist_map)
        for neighbor in neighbors:
            if neighbor in close_list:
                continue
            if exist_map[neighbor] == False:
                continue

            if neighbor not in open_list:
                open_list.append(neighbor)
                open_list[-1].parent = current
            elif neighbor.gn(start) > (current.gn(start) + dis(current, neighbor)):
                open_list[open_list.index(neighbor)].parent = current

    if end not in close_list:
        print "Path not found"
    else:
        print_path(start, end)
