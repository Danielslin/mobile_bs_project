# coding:UTF-8

import networkx as nx
import matplotlib.pyplot as plt
import tsp


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


def drawConvexHull(all_points, chPoints):
    G = nx.Graph()
    G.add_nodes_from(range(len(all_points)))
    pos = {}
    for i in range(len(all_points)):
        pos.update({i: (all_points[i].x, all_points[i].y)})

    for i in range(len(chPoints)):
        if i < len(chPoints) - 1:
            G.add_edge(all_points.index(chPoints[i]), all_points.index(chPoints[i + 1]))
        else:
            G.add_edge(all_points.index(chPoints[-1]), all_points.index(chPoints[0]))
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


a = tsp.rand_node_gen(100, 20)
s = tsp.graham_scan(a)
drawConvexHull(a, s)
plt.show()


# nodes = tsp.rand_node_gen(1000, 20)
# dis_matrix = tsp.dis_matrix(nodes)
# order_of_nodes = tsp.greedy_sol_tsp(dis_matrix)

# opt_show(dis_matrix, order_of_nodes)
# print "All random starts"
# opt_show(dis_matrix, range(len(nodes)))
# print "Greedy starts"
# opt_show(dis_matrix, order_of_nodes)
