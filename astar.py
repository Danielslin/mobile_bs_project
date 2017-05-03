# coding:UTF-8

from collections import defaultdict
import math


def manhattan_dis(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


def dis(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


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
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)

    def neighbors(self, exist_map):
        n = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if (x != self.x or y != self.y) and exist_map[AStarNode(x, y)] == True:
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
    parent_dict = {}
    open_list = [start]
    close_list = []
    count = 0
    print "A_star algorithm begins"
    while (len(open_list)) and (end not in close_list):
        count = count + 1
        print "\nloop " + str(count)
        open_list.sort(key=lambda node: node.fn(start, end))
        print "loop initial open:" + str(open_list)
        current = open_list[0]
        close_list.append(open_list.pop(0))
        print "current:" + str(current)
        print "put " + str(current) + " to close"
        print "close:" + str(close_list)
        neighbors = current.neighbors(exist_map)
        print "current neighbors:"
        print neighbors
        for neighbor in neighbors:
            if neighbor in parent_dict:
                neighbor.parent = parent_dict[neighbor]
            if neighbor in close_list:
                continue
            if exist_map[neighbor] == False:
                continue

            if neighbor not in open_list:
                open_list.append(neighbor)
                open_list[-1].parent = current
            elif neighbor.gn(start) > (current.gn(start) + dis(current, neighbor)):
                open_list[open_list.index(neighbor)].parent = current
                print "change " + str(neighbor) + "'s parent to " + str(current)
            parent_dict[neighbor] = neighbor.parent
            print str(neighbor) + " parent: " + str(neighbor.parent)

    if end not in close_list:
        print "Path not found"
    else:
        print_path(start, close_list[close_list.index(end)])
