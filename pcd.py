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


def fastPCD(polygon):
    concaves = []
    visible = {}
    a, b, c = {}, {}, {}
    sp = []
    # 搜索全部的凹点
    for vertex in polygon:
        if polygon.isConcavePoint(vertex):
            concaves.append(vertex)
    # 没有凹点则返回自身
    if not concaves:
        return polygon
    else:
        # 将可见点分成A、B、C三类
        for point in concaves:
            visible[point] = polygon.VisiblePoints(point)
            sa[point] = [p for p in visible[point] if cross_product(
                point, p, polygon.previousPoint(point)) * cross_product(
                    point, p, polygon.nextPoint(point)) < 0]
            sb[point] = [p for p in visible[point] if cross_product(
                point, p, polygon.previousPoint(point)) < 0 and cross_product(
                    point, p, polygon.nextPoint(point)) < 0]
            sc[point] = [p for p in visible[point] if cross_product(
                point, p, polygon.previousPoint(point)) > 0 and cross_product(
                    point, p, polygon.nextPoint(point)) > 0]
        for point in concaves:
            sp = []
            if sa[point]:
                for p in sa[point]:
                # 如果是p是凹点且当前点在p的a类中，则将p加入sp
                    if polygon.isConcavePoint(p) and point in sa[p]:
                        sp.append(p)
                if not sp:
                    sp = sa[point][:]
        # 如果集合SP中的顶点只有一个，则选中该点
        # 否则求出SP顶点中的权值
        # ……


'''
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
'''
