# coding:UTF-8
import numpy as np
import cv2
import math
from collections import deque
from polys import *

INFINITY = 99999.0

initEnergy = 1
E_elec = 5e-8
efs = 1e-11
emp = 1.3e-14
d0 = 87
defaultDataSize = 20


def dis(p1, p2):
    return int(math.hypot(p1[0] - p2[0], p1[1] - p2[1]))


class SensorNode(object):

    def __init__(self, location):
        self._loc = location
        self._energy = initEnergy

    @property
    def loc(self):
        return self._loc

    @property
    def x(self):
        return self._loc[0]

    @property
    def y(self):
        return self._loc[1]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y) + str(self._energy))

    def __str__(self):
        return "Sensor Node(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "Sensor Node(%s, %s)" % (self.x, self.y)

    @property
    def energy(self):
        return self._energy

    def recv(self, k):
        consumedEnergy = k * E_elec
        self._energy -= consumedEnergy

    def send(self, targetNode, k=defaultDataSize):
        d = dis(self._loc, targetNode.loc)
        if d < d0:
            consumedEnergy = k * (E_elec + efs * pow(d, 2))
        else:
            consumedEnergy = k * (E_elec + emp * pow(d, 4))
        self._energy -= consumedEnergy
        # targetNode.recv(k)


class Map(object):

    # areas:由点集组成的列表
    def __init__(self, areas):
        self.areas = areas
        self.path_length_limit = 4000

    def is_accessible(self, node):
        for area in self.areas:
            if cv2.pointPolygonTest(area.vertices, node, False) > 0:
                return True
        return False

    def random_node_gen(self, num):
        count = 0
        res = []
        while count < num:
            t = tuple(np.random.randint(1, 1079, 2))
            if self.is_accessible(t):
                res.append(t)
                count += 1
        self.nodes = res

    def init_sensors(self, num):
        if not hasattr(self, 'nodes'):
            self.random_node_gen(num)
        self._sensors_dict = {node: SensorNode(node) for node in self.nodes}
        self.sensors = [SensorNode(node) for node in self.nodes]

    # 覆盖范围C
    @staticmethod
    def covered(rp, node, C):
        # 坐标快速判断
        if abs(node[0] - rp[0]) > C or abs(node[1] - rp[1]) > C:
            return False
        # 坐标条件满足，再精确计算距离
        else:
            if dis(rp, node) > C:
                return False
        return True

    def nodes_belongs_to_poly(self):
        nodes = [[] for i in range(len(meshes))]
        if not hasattr(self, 'nodes'):
            raise Exception("nodes not generated")
        for node in self.nodes:
            nodes[belongs_to_polygon(node, meshes)].append(node)
        self.nodes_in_poly = nodes

    # 生成路径点
    # C:控制范围常数
    def rp_gen(self, C):

        # 覆盖节点数
        def cover_nodes(point):
            N = 0
            for node in self.nodes:
                if self.covered(point, node, C):
                    N += 1
            return N

        # 到已知点集的最短距离
        # 返回最近点与对应的最短距离的tuple
        def min_len_to_exist_RPs(point, RPs):
            # 以欧式距离初始化
            distances = {RP: dis(point, RP) for RP in RPs}
            path_found = {RP: False for RP in RPs}
            # 用寻路距离更新
            RP = (0, 0)
            while True:
                min_dis = min(distances.items(), key=lambda item: item[1])
                if RP == min_dis[0]:
                    return min_dis
                RP = min_dis[0]
                # 避免重复寻路
                if path_found[RP] is False:
                    distances[RP] = path_length(point, RP)
                    path_found[RP] = True

        # 每个网格取适应度最高点作为候选
        rp_candidate = []
        fitness = {}
        '''
        position = [(x, y) for x in range(area.minx, area.maxx, 60) for y in range(
                area.miny, area.maxy, 60) if self.is_accessible((x, y)) and cv2.pointPolygonTest(area.vertices, (x, y), False) > 0]
        '''
        position = [(x, y) for x in range(0, 1080, 100) for y in range(0, 1080, 100) if self.is_accessible((x, y))]
            # next_pos = max(position, key=cover_nodes)
        for next_pos in position:
            rp_candidate.append(next_pos)
            fitness[next_pos] = cover_nodes(next_pos)

        RPs = []
        # 第一个点
        RPs.append(max(rp_candidate, key=lambda pos: fitness[pos]))
        rp_candidate.remove(RPs[0])

        # 初始化
        # 防止重复计算
        covers = {rp: cover_nodes(rp) for rp in rp_candidate}
        # 防止重复计算路径
        distances = {}
        while True:
            # 更新适应度，适应度等于覆盖节点数 / 与已知RP的最小距离
            fitness = {
                rp: (float(covers[rp]) / len(self.nodes) * ((float(min_len_to_exist_RPs(rp, RPs)[1])) / self.path_length_limit)) for rp in rp_candidate}
            # 选择适应度最大点
            next_rp = max(rp_candidate, key=lambda rp: fitness[rp])
            # 选择合适的位置插入
            nearest_RP, min_len = min_len_to_exist_RPs(next_rp, RPs)
            if RPs[-1] == nearest_RP:
                RPs.append(next_rp)
            elif path_length(next_rp, RPs[RPs.index(nearest_RP) + 1]) > path_length(next_rp, RPs[RPs.index(nearest_RP) - 1]):
                RPs.insert(RPs.index(nearest_RP), next_rp)
            else:
                RPs.insert(RPs.index(nearest_RP) + 1, next_rp)
            new_path_len = 0
            for i in range(-1, len(RPs) - 1):
                if (RPs[i], RPs[i + 1]) not in distances:
                    distances[(RPs[i], RPs[i + 1])] = path_length(RPs[i], RPs[i + 1])
                new_path_len += distances[(RPs[i], RPs[i + 1])]
            if new_path_len > self.path_length_limit:
                RPs.remove(next_rp)
                rp_candidate.remove(next_rp)
                if not rp_candidate:
                    break
                continue
            else:
                path_len = new_path_len
                rp_candidate.remove(next_rp)
                if not rp_candidate:
                    break
        # 尝试凸包法
        '''
        TSP = tsp.tsp()
        TSP.exist_nodes(RPs)
        ch_RPs_order = [RPs[i] for i in TSP.convexhull()]
        ch_path_len = 0
        for i in range(-1, len(ch_RPs_order) - 1):
            if (ch_RPs_order[i], ch_RPs_order[i + 1]) not in distances:
                distances[(ch_RPs_order[i], ch_RPs_order[i + 1])] = path_length(ch_RPs_order[i], ch_RPs_order[i + 1])
            ch_path_len += distances[(ch_RPs_order[i], ch_RPs_order[i + 1])]
        print "Convex hull TSP solution path length:", ch_path_len
        print "Greedy TSP solution path length:", path_len
        '''
        point_order = []
        for i in range(-1, len(RPs) - 1):
            point_order += find_path(RPs[i], RPs[i + 1])

        self.RPs = RPs
        return path_len, RPs, point_order

    # 生成路由
    def routing(self, routing_radius):

        # 更新距离最近的路径点
        sensors_belong_to_RP = []
        for RP in self.RPs:
            sensors_belong_to_RP.append([])
        min_dis_to_RPs = {}
        for sensor in self.sensors:
            min_dis_to_RPs[sensor] = (INFINITY, -1)
            for index_RP, RP in enumerate(self.RPs):
                d = dis(sensor.loc, RP)
                if d < min_dis_to_RPs[sensor][0]:
                    min_dis_to_RPs[sensor] = (d, index_RP)
            sensors_belong_to_RP[min_dis_to_RPs[sensor][1]].append(sensor)

        route = {}
        has_visited = {sensor: False for sensor in self.sensors}
        for index_RP, sensors in enumerate(sensors_belong_to_RP):
            queue = deque()
            queue.append(SensorNode(self.RPs[index_RP]))
            while queue:
                curr_node = queue.popleft()
                for sensor in sensors:
                    if dis(sensor.loc, curr_node.loc) < routing_radius and has_visited[sensor] is False and sensor != curr_node:
                        route[sensor] = curr_node
                        queue.append(sensor)
                        has_visited[sensor] = True
        # 剩下未路由的节点选择最近点作为路由
        for sensor in sorted(self.sensors, key=lambda x: min_dis_to_RPs[x][0]):
            if has_visited[sensor] is False:
                route[sensor] = SensorNode(self.RPs[min_dis_to_RPs[sensor][1]])
                for node in self.sensors:
                    if dis(node.loc, sensor.loc) < dis(route[sensor].loc, sensor.loc) and node != sensor and has_visited[node]:
                        route[sensor] = node
                        has_visited[sensor] = True
        self.routes = route
        return route

    # 能耗仿真
    # 一个节点通过路由将k bit的数据包传输到RP
    def transfer_data(self, sensor_node, k):
        if sensor_node.loc in self.RPs:
            return
        else:
            sensor_node.send(self.routes[sensor_node], k)
        if self.routes[sensor_node].loc not in self.RPs:
            self.routes[sensor_node].recv(k)

        # 递归
        self.transfer_data(self.routes[sensor_node], k)
