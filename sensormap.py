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
                    raise TypeError('vertex is not Point_2D')
        self.V = list(set(vertexes))
        self.V.sort(cmp=cmp_x)
        self.V[1:] = sorted(self.V[1:], cmp=lambda x,
                            y: cmp_angle(x, y, self.V[0]))
        self.edges = []

    def __getitem__(self, index):
        return self.V[index]

    def __len__(self):
        return len(self.V)

    def __add__(self, other_poly):
        self.V.extend(other_poly.V)
        return SimplePolygon(self.V)

    def __iter__(self):
        return iter(self.V)

    def next(self):
        return iter(self.V).next()

    def index(self, vertex):
        return self.V.index(vertex)

    def addPoint(self, point):
        if not isinstance(point, Point_2D):
            raise TypeError('vertex is not Point_2D')
        if point not in self.V:
            self.V.append(point)
            V0 = self.V[1:]
            V0.sort(lambda x, y: cmp_angle(x, y, self.V[0]))
            self.V[1:] = V0

    def delPoint(self, point):
        if point in self.V:
            self.V.remove(point)

    def nextPoint(self, point):
        if self.index(point) == len(self) - 1:
            return self[0]
        else:
            return self[self.index(point) + 1]

    def previousPoint(self, point):
        if self.index(point) == 0:
            return self[-1]
        else:
            return self[self.index(point) - 1]

    def get_edges(self):
        e = []
        for i, vertex in enumerate(self.V):
            if i != len(self.V) - 1:
                e.append(segment(vertex, self.V[i + 1]))
            else:
                e.append(segment(vertex, self.V[0]))
        self.edges = e
        return e

    def pos(self):
        return {i: (i.x, i.y) for i in self.V}

    def draw(self):
        G = nx.Graph()
        G.add_nodes_from(range(len(self.V)))
        pos = {i: (self[i].x, self[i].y) for i in range(len(self))}
        for i in range(len(self)):
            if i < len(self) - 1:
                G.add_edge(i, i + 1)
            else:
                G.add_edge(i, 0)
        nx.draw(G, pos, with_labels=True)
        return G

    def isConcavePoint(self, point):
        if point in self.V:
            i = self.V.index(point)
            if i > 0 and i < len(self.V) - 1:
                return (cross_product(self.V[i - 1], self.V[i + 1], self.V[i]) > 0)
            elif i == 0:
                return (cross_product(self.V[-1], self.V[1], self.V[0]) > 0)
            elif i == len(self.V) - 1:
                return (cross_product(self.V[-2], self.V[0], self.V[-1]) > 0)
            else:
                raise Exception('point not in polygon')

    def pointInPoly(self, point):
        if not self.edges:
            self.get_edges()
        count = 0
        seg = segment(Point_2D(0, point.y), point)
        for edge in self.edges:
            if edge.pointInSegment(point):
                return True
            if edge.pb.x != edge.pa.x:
                if (seg.pointInSegment(edge.pa) and edge.maxY() == edge.pa.y) or (
                        seg.pointInSegment(edge.pb) and edge.maxY() == edge.pb.y):
                    count += 1
                elif isIntersect(seg, edge):
                    count += 1
        return count % 2 != 0

    def isVisible(self, ViewPoint, TargetPoint):
        if not self.edges:
            self.get_edges()
        if ViewPoint == TargetPoint:
            return True
        seg = segment(ViewPoint, TargetPoint)
        for edge in self.edges:
            if isIntersect(seg, edge):
                ints = Intersection(seg, edge)
                if ints and ints != seg.pa and ints != seg.pb:
                    return False
                if not self.pointInPoly(seg.midPoint()):
                    return False
        return True

    def VisiblePoints(self, ViewPoint):
        return [point for point in self.V if self.isVisible(ViewPoint, point)]


class Map(object):

    def __init__(self, size_of_map, res=10):
        if math.log10(res) not in RES_CLASS:
            raise ValueError('resolution out of range')
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


test = tsp()
mapsize = 1000
test.randomnodes(mapsize, 20)
poly1 = SimplePolygon(*test.nodes)

for point in poly1:
    print poly1.index(point)
    print poly1.previousPoint(point)
    print poly1.nextPoint(point)
poly1.draw()
plt.show()
