# coding:UTF-8

# Drawing
import networkx as nx
import matplotlib.pyplot as plt
import convexhull as ch
import tsp

nodes = tsp.read_tsplib('TSPlib/oliver30.tsp')


def drawTSPGraph(nodes, order_of_nodes):
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


# 测试TSP 凸包算法

greedy = tsp.greedy_sol_tsp(nodes)
G = drawTSPGraph(nodes, greedy)
plt.savefig("TSPcomparison/01_greedySolvedTSP.png", dpi=256)
plt.show()

greedy_opt = tsp.opt(nodes, greedy, 100000)
G = drawTSPGraph(nodes, greedy_opt)
plt.savefig("TSPcomparison/02_2-opted_greedySolvedTSP.png", dpi=256)
plt.show()

gs = ch.drawConvexHull(nodes)
plt.show()

ch = tsp.ch_sol_tsp(nodes)
G = drawTSPGraph(nodes, ch)
plt.savefig("TSPcomparison/03_chSolvedTSP.png", dpi=256)
plt.show()

ch_opt = tsp.opt(nodes, ch, 100000)
G = drawTSPGraph(nodes, ch_opt)
plt.savefig("TSPcomparison/04_2-opted_chSolvedTSP.png", dpi=256)
plt.show()
