# coding:utf-8

# points of polys and bridges
import numpy as np
import cv2
import math


class Polygon(object):

    def __init__(self, vertices):
        self.vertices = np.array(vertices).reshape(-1, 1, 2)

    @property
    def minx(self):
        return min([g[0] for g in self.vertices.reshape(-1, 2)])

    @property
    def maxx(self):
        return max([g[0] for g in self.vertices.reshape(-1, 2)])

    @property
    def miny(self):
        return min([g[1] for g in self.vertices.reshape(-1, 2)])

    @property
    def maxy(self):
        return max([g[1] for g in self.vertices.reshape(-1, 2)])

    @property
    def moments(self):
        return cv2.moments(self.vertices)

    @property
    def center(self):
        return (int(self.moments['m10'] / self.moments['m00']), int(self.moments['m01'] / self.moments['m00']))

    @property
    def edges(self):
        return [(self.vertices[x], self.vertices[x + 1]) for x in range(-1, len(self.vertices) - 1)]


    def distance_to(self, other_polygon):
        res = cv2.pointPolygonTest(other_polygon.vertices, self.center, True)
        if res > 0:
            res = 0
        else:
            res = -res
        return res
    '''
    # 多边形中心的距离
    def distance_to(self, other_polygon):
        return math.hypot((self.center()[0] - other_polygon.center()[0]),
                          (self.center()[1] - other_polygon.center()[1]))
    '''


def dis(p1, p2):
    if p1 == p2:
        return 0.0
    else:
        return int(math.hypot((p1[0] - p2[0]), (p1[1] - p2[1])))


def cross_product(v1, v2):
    return np.linalg.det((v1, v2))


# 多边形顶点
p = [[(1, 1), (1, 210), (189, 284), (189, 1)],  # 1
     [(189, 1), (189, 284), (334, 392), (334, 1)],  # 2
     [(715, 486), (715, 1), (334, 1), (334, 392)],  # 3
     [(937, 428), (937, 1), (715, 1), (715, 486)],  # 4
     [(937, 1), (937, 428), (1078, 336), (1078, 1)],  # 5
     [(1078, 336), (937, 428), (888, 507), (862, 627), (1078, 647)],  # 6
     [(888, 507), (657, 548), (728, 659), (789, 670), (862, 627)],  # 7
     [(657, 548), (703, 694), (728, 659)],  # 8
     [(657, 548), (509, 735), (606, 783), (721, 751)],  # 9
     [(657, 548), (392, 472), (327, 480), (304, 528), (362, 751), (509, 735)],  # 10
     [(304, 528), (166, 460), (87, 506), (282, 814), (362, 751)],  # 11
     [(87, 506), (134, 953), (262, 876), (282, 814)],  # 12
     [(87, 506), (1, 470), (1, 757), (62, 771), (101, 650)],  # 13
     [(101, 650), (62, 771), (49, 935), (81, 1017), (134, 953)],  # 14
     [(134, 953), (220, 1004), (310, 940), (262, 876)],  # 15
     [(310, 940), (220, 1004), (381, 972), (395, 938)],  # 16
     [(406, 997), (337, 1025), (292, 1079), (406, 1079)],  # 17
     [(517, 926), (458, 952), (406, 997), (406, 1079), (517, 1079)],  # 18
     [(616, 876), (517, 926), (517, 1079), (669, 1079), (669, 881)],  # 19
     [(669, 881), (669, 1079), (773, 1079), (773, 891), (751, 863), (730, 858)],  # 20
     [(773, 1079), (1078, 1079), (942, 921), (856, 874), (773, 891)],  # 21
     [(1078, 984), (1037, 932), (942, 921), (1078, 1079)]]  # 22
b = [[(240, 322), (222, 308), (177, 465), (196, 475)],  # 23
     [(429, 416), (407, 410), (393, 473), (416, 478)],  # 24
     [(524, 439), (504, 434), (489, 500), (510, 505)],  # 25
     [(780, 470), (756, 475), (771, 527), (794, 523)],  # 26
     [(689, 760), (667, 766), (684, 875), (706, 868)],  # 27
     [(365, 975), (347, 979), (347, 1022), (365, 1013)]]  # 28
polys = [Polygon(poly) for poly in p]
navmeshes = [Polygon(poly) for poly in p] + [Polygon(bridge) for bridge in b]

# 邻接表待改

neighbor_list = [(0, 1), (1, 2), (1, 22), (2, 3), (2, 23), (2, 24),
                 (3, 4), (3, 25), (4, 5), (5, 6), (6, 7), (6, 25),
                 (7, 8), (8, 9), (8, 26), (9, 10), (9, 23), (9, 24),
                 (10, 11), (10, 22), (11, 12), (11, 13), (11, 14),
                 (12, 13), (14, 15), (15, 27), (16, 17), (16, 27),
                 (17, 18), (18, 19), (19, 20), (19, 26), (20, 21)]
neighbor_list.extend([(x[1], x[0]) for x in neighbor_list])
neighbor_list.sort(key=lambda x: x[0])


def belongs_to_polygon(point, meshes=navmeshes):
    # 返回所在的mesh的下标
    for mesh in meshes:
        if point[0] > mesh.maxx or point[0] < mesh.minx or point[1] > mesh.maxy or point[1] < mesh.miny:
            continue
        if cv2.pointPolygonTest(mesh.vertices, point, False) >= 0:
            return meshes.index(mesh)


# 基于导航网格的A*寻路
def astar(start_point, end_point, meshes=navmeshes, neighbors=neighbor_list):

    def g(mesh):
        if mesh == start_mesh:
            return 0
        return meshes[mesh].distance_to(meshes[father[mesh]]) + g(father[mesh])

    def h(mesh):
        return meshes[mesh].distance_to(meshes[end_mesh])

    def f(mesh):
        return g(mesh) + h(mesh)

    def get_route(mesh):
        if mesh == start_mesh:
            return [start_mesh]
        else:
            return get_route(father[mesh]) + [mesh]

    start_mesh = belongs_to_polygon(start_point, meshes)
    end_mesh = belongs_to_polygon(end_point, meshes)
    if start_mesh is None or end_mesh is None:
        raise Exception('inaccessible start point or end point')
    if start_mesh == end_mesh:
        return [start_mesh]
    open_list, close_list = [start_mesh], []
    father = {}

    while end_mesh not in close_list:
        if not open_list:
            return None
        current_mesh = min(open_list, key=f)
        for edge in neighbors:
            # 找当前点的所有邻接点
            if edge[0] == current_mesh:
                if edge[1] in close_list:
                    continue
                if edge[1] not in open_list:
                    open_list.append(edge[1])
                    father[edge[1]] = current_mesh
                else:
                    if meshes[edge[1]].distance_to(meshes[current_mesh]) + g(current_mesh) < g(edge[1]):
                        father[edge[1]] = current_mesh
        open_list.remove(current_mesh)
        close_list.append(current_mesh)
    if end_mesh in close_list:
        return get_route(end_mesh)


# 初始化邻接边表

adjacent_edges = {}
for poly in navmeshes:
    for neighbor in neighbor_list:
        if neighbor[0] == navmeshes.index(poly):
            for edge in poly.edges:
                if abs(cv2.pointPolygonTest(navmeshes[neighbor[1]].vertices, tuple(edge[0].reshape(-1)), True) + cv2.pointPolygonTest(navmeshes[neighbor[1]].vertices, tuple(edge[1].reshape(-1)), True)) <= 10:
                    adjacent_edges[neighbor] = (
                        tuple(edge[0].reshape(-1)), tuple(edge[1].reshape(-1)))

for x, y in neighbor_list:
    if (x, y) not in adjacent_edges.keys():
        adjacent_edges[(x, y)] = (adjacent_edges[(y, x)]
                                  [1], adjacent_edges[(y, x)][0])

# 寻找避障路径
def find_path(start_point, end_point, meshes=navmeshes, neighbors=neighbor_list, adjacent_edges=adjacent_edges):

    def vector(point_pair):
        return (point_pair[1][0] - point_pair[0][0], point_pair[1][1] - point_pair[0][1])

    point_order = [start_point, end_point]
    mesh_order = astar(start_point, end_point, meshes, neighbors)
    if not mesh_order:
        return None
    # 如果在同一网格内则可直达，无须避障
    if len(mesh_order) == 1:
        return point_order

    leftPoints, rightPoints = [], []
    for i in range(len(mesh_order) - 1):
        adjacent_edge = adjacent_edges[(mesh_order[i], mesh_order[i + 1])]
        rightPoints.append(adjacent_edge[0])
        leftPoints.append(adjacent_edge[1])

    current_point = start_point
    currentLeftPoint, currentRightPoint = leftPoints[0], rightPoints[0]
    i = 0
    while i < len(leftPoints) - 1:
        nextLeftPoint, nextRightPoint = leftPoints[i + 1], rightPoints[i + 1]
        lineRight = vector((current_point, currentRightPoint))
        lineLeft = vector((current_point, currentLeftPoint))
        nextLineRight = vector((current_point, nextRightPoint))
        nextLineLeft = vector((current_point, nextLeftPoint))
        # 如果新左或右点在左右线之间，更新之
        if cross_product(lineLeft, nextLineLeft) * cross_product(lineRight, nextLineLeft) <= 0:
            currentLeftPoint = nextLeftPoint
        if cross_product(lineLeft, nextLineRight) * cross_product(lineRight, nextLineRight) <= 0:
            currentRightPoint = nextRightPoint
        # 如果新左右点都在左线或右线之外，增加拐点
        if cross_product(lineLeft, nextLineLeft) < 0 and cross_product(lineLeft, nextLineRight) < 0:
            point_order.insert(-1, currentLeftPoint)
            current_point = currentLeftPoint
            i = leftPoints.index(current_point) + 1
            currentLeftPoint = leftPoints[i]
            currentRightPoint = rightPoints[i]
            continue
        if cross_product(lineRight, nextLineRight) > 0 and cross_product(lineRight, nextLineLeft) > 0:
            point_order.insert(-1, currentRightPoint)
            current_point = currentRightPoint
            i = rightPoints.index(current_point) + 1
            currentLeftPoint = leftPoints[i]
            currentRightPoint = rightPoints[i]
            continue
        i += 1
    lineRight = vector((current_point, currentRightPoint))
    lineLeft = vector((current_point, currentLeftPoint))
    if cross_product(vector((current_point, end_point)), lineLeft) > 0 and cross_product(vector((current_point, end_point)), lineRight) > 0:
        point_order.insert(-1, currentLeftPoint)
    if cross_product(vector((current_point, end_point)), lineLeft) < 0 and cross_product(vector((current_point, end_point)), lineRight) < 0:
        point_order.insert(-1, currentRightPoint)
    return point_order

def path_length(start_point, end_point, meshes=navmeshes, neighbors=neighbor_list, adjacent_edges=adjacent_edges):
    length = 0
    path = find_path(start_point, end_point, navmeshes, neighbor_list, adjacent_edges)
    for i in range(len(path) - 1):
        length += dis(path[i], path[i + 1])
    return length


if __name__ == '__main__':
    pointA, pointB = (240, 840), (360, 960)
    print astar(pointA, pointB)
    print find_path(pointA, pointB)
    print path_length(pointA, pointB)
