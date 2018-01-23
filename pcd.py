# coding:UTF-8

import sensormap
import networkx as nx
import matplotlib.pyplot as plt
import tsp
from geoop import *
from point2d import *


def Rogers(polygon):
    if not isinstance(polygon, sensormap.SimplePolygon):
        raise TypeError('must run on simple polygon')
    result = [polygon]
    poly = polygon
    edges = poly.get_edges()
    d = 10000000
    t, dec_point = Point_2D(0, 0), None
    for i in range(len(poly)):
        if poly.isConcavePoint(poly[i]):
            result = []
            if i != 0:
                seg = segment(poly[i - 1], poly[i])
            else:
                seg = segment(poly[-1], poly[0])
            rad = segment(seg.pb, (seg.pb - seg.pa) * 100000 + seg.pa)
            for edge in edges:
                if isIntersect(rad, edge):
                    t = Intersection(rad, edge)
                    if dis(t, seg.pb) < d:
                        d = dis(t, seg.pb)
                        dec_point = t
            poly.addPoint(dec_point)
            res1 = sensormap.SimplePolygon(*poly[:poly.index(dec_point) + 1])
            res2 = sensormap.SimplePolygon(*poly[poly.index(dec_point):])
            result.extend(Rogers(res1))
            result.extend(Rogers(res2))

    return result


test = tsp.tsp()
mapsize = 1000
test.randomnodes(mapsize, 20)
poly1 = sensormap.SimplePolygon(*test.nodes)

graphs = [poly1.draw()]
plt.show()

ress = Rogers(poly1)
pos = {}
for poly in ress:
    graphs.append(poly.draw())
    pos.update(poly.pos())
graph = nx.compose_all(graphs)
nx.convert_node_labels_to_integers(graph)
nx.draw(graph, pos, with_labels=False)
plt.show()
