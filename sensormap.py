# coding:UTF-8

# Sensor map Initialzation
import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import convexhull as ch
from point2d import *
from tsp import *

RES_CLASS = range(5)


class MapNode(Point_2D):

    def __init__(self, x, y):
        Point_2D.__init__(self, x, y)
        self.location = (x, y)
        self._isBarrier = False

    def __str__(self):
        return "MapNode(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "MapNode(%s, %s)" % (self.x, self.y)

    def isBarrier(self):
        return self._isBarrier

    def SetToBarrier(self):
        self._isBarrier = True


class SensorNode(Point_2D):

    def __init__(self, x, y, ID=None):
        Point_2D.__init__(self, x, y)
        self._energy = 10
        self.id = ID

    def __str__(self):
        return "Sensor node %s (%s, %s)" % (self.id, self.x, self.y)

    def __repr__(self):
        return "Sensor node %s (%s, %s)" % (self.id, self.x, self.y)

    def energy(self):
        return self._energy


class SimplePolygon(object):
    # vertexes:list of Point_2D
    def __init__(self, *vertexes):
        if len(vertexes) > 0:
            for vertex in vertexes:
                if not isinstance(vertex, Point_2D):
                    raise TypeError
        self.V = list(vertexes)
        self.V.sort(cmp=cmp_x)
        self.V[1:] = sorted(self.V[1:], cmp=lambda x, y: cmp_angle(x, y, self.V[0]))

    def add(self, point):
        if not isinstance(point, Point_2D):
            raise TypeError
        if point not in self.V:
            self.V.append(point)
            V0 = self.V[1:]
            V0.sort(lambda x, y: cmp_angle(x, y, self.V[0]))
            self.V[1:] = V0

    def delete(self, point):
        if point in self.V:
            self.V.remove(point)

    def draw(self):
        G = nx.DiGraph()
        G.add_nodes_from(range(len(self.V)))
        pos = {i: (self.V[i].x, self.V[i].y) for i in range(len(self.V))}
        for i in range(len(self.V)):
            if i < len(self.V) - 1:
                G.add_edge(i, i + 1)
            else:
                G.add_edge(i, 0)
        nx.draw(G, pos, with_labels=True)
        return G


class Map(object):

    def __init__(self, size_of_map, res=10):

        if math.log10(res) not in RES_CLASS:
            raise ValueError
        self._accuracy = int(math.log10(res))
        self.size = size_of_map
        self.res = float(res)
        self._map = {}
        for i in range(self.size * res):
            for j in range(self.size * res):
                self._map[(i / self.res, j / self.res)
                          ] = MapNode(i / self.res, j / self.res)

    def map(self, x, y):
        X, Y = round(x, self._accuracy), round(y, self._accuracy)
        return self._map[(X, Y)]

    def InitBarrier(self, barrier_map):
        # barrier_map: [(x1,y1), (x2,y2), ...]
        for map_node in barrier_map:
            self._map[map_node].SetToBarrier()

    def InitSensors(self, node_amount):
        self.sensors = []
        while len(self.sensors) < node_amount:
            count = 0
            X = random.uniform(0, self.size)
            Y = random.uniform(0, self.size)
            if self.map(X, Y).isBarrier():
                continue
            self.sensors.append(SensorNode(X, Y, count))
            count += 1
        return self.sensors

# test code


test = tsp()
mapsize = 1000
test.randomnodes(mapsize, 20)
poly1 = SimplePolygon(*test.nodes)
poly1.draw()
plt.show()
'''
poly2 = SimplePolygon(*ch.graham_scan(poly1.V))
poly2.draw()
plt.show()
'''
'''
poly.add(RandomNode(mapsize))
poly.draw()
plt.show()
'''
