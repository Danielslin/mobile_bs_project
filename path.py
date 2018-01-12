# coding:UTF-8

from point2d import *
from tsp import *
import random
import networkx as nx
import matplotlib.pyplot as plt


# 默认起点为第一个点，终点为最后一个点
def opt_shortest_path(points):
    t = tsp()
    t.nodes = points
    t.order = range(len(t.nodes))
    t.dismatrix()
    # 2-opt法找到最短路径
    count = 0
    while(count < 100000):
        former_sum = t.sum(tsp=False)
        opted_order = t.order[:]
        # 随机生成两个交换的元素，起点终点不交换
        left, right = random.randint(
            1, len(t.order) - 2), random.randint(1, len(t.order) - 2)
        # 防止左边界比右边界大
        if left > right:
            left, right = right, left
        # 左右边界之间的序列反转
        temp = opted_order[left:right + 1]
        temp.reverse()
        opted_order[left:right + 1] = temp
        # 对新序列求和
        if t.sum(opted_order, tsp=False) < former_sum:
            t.order = opted_order
            count = 0
        else:
            count += 1
    return t.order


def DrawPath(nodes, order_of_nodes):
    G = nx.DiGraph()                 # 建立一个空的有向图G
    G.add_nodes_from(range(len(nodes)))
    pos = {i: (nodes[i].x, nodes[i].y) for i in range(len(nodes))}
    for i in range(len(nodes)):
        if i < len(nodes) - 1:
            G.add_edge(order_of_nodes[i], order_of_nodes[i + 1])
    nx.draw(G, pos, with_labels=True, font_size=12, node_size=96)
    return G


test = tsp()
test.randomnodes(100, 10)
test.order = range(len(test.nodes))
test.dismatrix()
DrawPath(test.nodes, test.order)
print "Random Path:", test.sum(tsp=False)
plt.show()

test.order = opt_shortest_path(test.nodes)
DrawPath(test.nodes, test.order)
print "Opted Path:", test.sum(tsp=False)
plt.show()
