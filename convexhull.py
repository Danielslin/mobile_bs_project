# coding:UTF-8
from point2d import *
from geoop import *
import networkx as nx


# 找出Graham算法的p0点
def p0_point(list_of_points):
    p0 = list_of_points[0]
    for point in list_of_points:
        if point.y < p0.y:
            p0 = point
        elif point.y == p0.y:
            if point.x < p0.x:
                p0 = point

    return p0


# Graham扫描算法计算凸包，返回Point2D对象组成的list
def graham_scan(list_of_points):
    stack = []
    p0 = p0_point(list_of_points)
    stack.append(p0)
    points = list_of_points[:]
    points.remove(p0)
    # 将点按以p0为参考点从右到左排序
    points.sort(lambda x, y: cmp_angle(x, y, p0))
    stack.extend(points[0:2])
    for point in points[2:]:
        while(cross_product(point, stack[-1], stack[-2]) > 0):
            stack.pop(-1)
        stack.append(point)

    return stack


# 画凸包，返回一个图对象
def DrawConvexHull(all_points):
    chPoints = graham_scan(all_points)
    G = nx.Graph()
    G.add_nodes_from(range(len(all_points)))
    pos = {}
    for i in range(len(all_points)):
        pos.update({i: (all_points[i].x, all_points[i].y)})

    for i in range(len(chPoints)):
        if i < len(chPoints) - 1:
            G.add_edge(all_points.index(
                chPoints[i]), all_points.index(chPoints[i + 1]))
        else:
            G.add_edge(all_points.index(
                chPoints[-1]), all_points.index(chPoints[0]))
    nx.draw(G, pos, with_labels=True, font_size=12, node_size=48)
    return G
