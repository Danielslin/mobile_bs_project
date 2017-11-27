# coding:UTF-8

import networkx as nx
import matplotlib.pyplot as plt
import tsp


def drawGraph(nodes, order_of_nodes):
    G = nx.DiGraph()                 # 建立一个空的无向图G
    G.add_nodes_from(range(len(nodes)))
    pos = {}
    for i in range(len(nodes)):
        pos.update({i: (nodes[i].x, nodes[i].y)})
        if i < len(nodes) - 1:
            G.add_edge(order_of_nodes[i], order_of_nodes[i + 1])
        else:
            G.add_edge(order_of_nodes[-1], order_of_nodes[0])
    nx.draw(G, pos, with_labels=True, font_size=16, node_size=48)


def opt_show(dis_matrix, init_order):

    turns = [0, 10, 50, 100, 200, 500, 1000]
    opted_order = init_order[:]
    for i in turns:
        opted_order = tsp.opt(dis_matrix, opted_order, i)
        print opted_order
        print tsp.sum_dis(dis_matrix, opted_order)
        drawGraph(nodes, opted_order)
        plt.savefig("opted" + str(i) + ".png", dpi=256)
        plt.show()


nodes = tsp.rand_node_gen(200, 50)
dis_matrix = tsp.dis_matrix(nodes)
order_of_nodes = tsp.greedy_sol_tsp(dis_matrix)

opt_show(dis_matrix, order_of_nodes)
