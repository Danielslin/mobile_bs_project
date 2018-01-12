# coding:UTF-8
# TSP solutions

import random
import networkx as nx
from point2d import *
from geoop import *
import convexhull as ch
INFINITY = 9999.0


class tsp(object):

    def __init__(self):
        self.nodes = []
        self.order = []
        self._solution = ''
        self._dismatrix = []

    def randomnodes(self, mapsize, nodeamount):
        self.nodes = RandomNodeGeneration(mapsize, nodeamount)

    def readfile(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        cut_off = lines.index('NODE_COORD_SECTION\n') + 1
        EOF = lines.index('EOF\n')
        lines = lines[cut_off:EOF]
        nodes = [Point_2D(x=float(line.strip().split()[1]),y=float(line.strip().split()[2])) for line in lines]
        self.nodes = nodes
        return nodes

    def dismatrix(self):
        if not self.nodes:
            pass
        dis_matrix = []
        for num, node in enumerate(self.nodes):
            dis_matrix.append([])
            for i in range(len(self.nodes)):
                if i < num:
                    dis_matrix[num].append(dis_matrix[i][num])
                elif i == num:
                    dis_matrix[num].append(INFINITY)
                else:
                    dis_matrix[num].append(dis(node, self.nodes[i]))
        self._dismatrix = dis_matrix
        return dis_matrix

    def sum(self, order=None, **kw):
        if order is None:
            order = self.order
        sum = 0
        for i in range(len(order)):
            if i >= len(order) - 1:
                if 'tsp' in kw and kw['tsp'] is False:
                    continue
                else:
                    sum += self._dismatrix[order[i]][order[0]]
            else:
                sum += self._dismatrix[order[i]][order[i + 1]]
        return sum

    def greedy(self):
        if not self.nodes:
            pass
        if not self._dismatrix:
            self.dismatrix()
        d_matrix = self._dismatrix
        reached_nodes = []
        current_node = 0
        next_node = 0
        t = []
        while (len(reached_nodes) < len(d_matrix) - 1):
            t = d_matrix[current_node][:]
            t.sort()
            reached_nodes.append(current_node)
            while(next_node in reached_nodes):
                next_node = d_matrix[current_node].index(t.pop(0))
            current_node = next_node
        reached_nodes.append(current_node)
        self.order = reached_nodes
        self._solution = 'Greedy'
        print "Greedy Solution:", reached_nodes, self.sum()
        return reached_nodes

    def convexhull(self):
        if not self.nodes:
            pass
        if not self._dismatrix:
            self.dismatrix()
        d_matrix = self._dismatrix
        chNodes = ch.graham_scan(self.nodes)
        reached_nodes = [self.nodes.index(node) for node in chNodes]
        unreached_nodes = [i for i in range(len(self.nodes)) if i not in reached_nodes]
        insert_cost = {}
        insert_cost = insert_cost.fromkeys(unreached_nodes, (INFINITY, (0, 0)))
        u, v = 0, 0
        while(unreached_nodes):
            for i in range(len(reached_nodes)):
                if i == len(reached_nodes) - 1:
                    u, v = reached_nodes[i], reached_nodes[0]
                else:
                    u, v = reached_nodes[i], reached_nodes[i + 1]

                for node in unreached_nodes:
                    t = d_matrix[u][node] + d_matrix[v][node] - d_matrix[u][v]
                    if t < insert_cost[node][0]:
                        insert_cost[node] = t, (u, v)
            costs = sorted(insert_cost.items(), key=lambda x: x[1][0])
            reached_nodes.insert(reached_nodes.index(costs[0][1][1][1]), costs[0][0])
            unreached_nodes.remove(costs[0][0])
            insert_cost.pop(costs[0][0])
        self.order = reached_nodes
        self._solution = "Convex Hull"
        print "Convex Hull Solution:", reached_nodes, self.sum()
        return reached_nodes

    def opt(self, limit=1000):
        if not (self.nodes or self.order):
            pass
        former_order = self.order[:]
        count = 0
        while(count < limit):
            former_sum = self.sum(former_order)
            opted_order = former_order[:]
        # 随机生成两个交换的元素
            left, right = random.randint(
                0, len(former_order) - 1), random.randint(0, len(former_order) - 1)
        # 防止左边界比右边界大
            if left > right:
                left, right = right, left
        # 左右边界之间的序列反转
            t = opted_order[left:right + 1]
            t.reverse()
            opted_order[left:right + 1] = t
        # 对新序列求和
            if self.sum(opted_order) < former_sum:
                former_order = opted_order
                count = 0
            else:
                count += 1

        self.order = former_order
        print "2-opted Solution:", former_order, former_sum
        return former_order

    def draw(self):
        nodes = self.nodes
        order_of_nodes = self.order
        G = nx.DiGraph()                 # 建立一个空的有向图G
        G.add_nodes_from(range(len(nodes)))
        pos = {i: (nodes[i].x, nodes[i].y) for i in range(len(nodes))}
        for i in range(len(nodes)):
            if i < len(nodes) - 1:
                G.add_edge(order_of_nodes[i], order_of_nodes[i + 1])
            else:
                G.add_edge(order_of_nodes[-1], order_of_nodes[0])
        nx.draw(G, pos, with_labels=True, font_size=12, node_size=48)
        return G
