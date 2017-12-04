# coding:UTF-8

import networkx as nx
import matplotlib.pyplot as plt
import tsp

nodes = tsp.rand_node_gen(1000, 20)


def drawTSPGraph(nodes, order_of_nodes):
    G = nx.DiGraph()                 # 建立一个空的有向图G
    G.add_nodes_from(range(len(nodes)))
    pos = {}
    for i in range(len(nodes)):
        pos.update({i: (nodes[i].x, nodes[i].y)})
        if i < len(nodes) - 1:
            G.add_edge(order_of_nodes[i], order_of_nodes[i + 1])
        else:
            G.add_edge(order_of_nodes[-1], order_of_nodes[0])
    nx.draw(G, pos, with_labels=True, font_size=12, node_size=48)


def opt_show(dis_matrix, init_order):

    turns = [0, 10, 50, 100, 200, 500, 1000, 10000, 100000]
    opted_order = init_order[:]
    for i in turns:
        opted_order = tsp.opt(dis_matrix, opted_order, i)
        print opted_order
        print "Iteration limit", i, ":", tsp.sum_dis(dis_matrix, opted_order)
        drawTSPGraph(nodes, opted_order)
        plt.savefig("opted" + str(i) + ".png", dpi=256)
        plt.show()


# 测试凸包算法
'''
s = tsp.graham_scan(nodes)
G = tsp.drawConvexHull(nodes)
plt.show()
'''

# 测试TSP 2-opt算法

'''
dis_matrix = tsp.dis_matrix(nodes)
print "All random starts"
opt_show(dis_matrix, range(len(nodes)))
print "Greedy starts"
opt_show(dis_matrix, order_of_nodes)
'''

dis_matrix = tsp.dis_matrix(nodes)
tsp.ch_sol_tsp(dis_matrix, nodes)
