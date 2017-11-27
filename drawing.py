# coding:UTF-8

import networkx as nx
import matplotlib.pyplot as plt
import tsp


nodes = tsp.rand_node_gen(100, 20)
dis_matrix = tsp.dis_matrix(nodes)
reached_nodes, sum_dis = tsp.greedy_sol_tsp(dis_matrix)
print reached_nodes
print sum_dis

G = nx.Graph()                 # 建立一个空的无向图G
G.add_nodes_from(range(len(nodes)))
pos = {}
for i in range(len(nodes)):
    pos.update({i: (nodes[i].x, nodes[i].y)})
    if i < len(nodes) - 1:
        G.add_edge(reached_nodes[i], reached_nodes[i + 1])
    else:
        G.add_edge(reached_nodes[-1], reached_nodes[0])

print "nodes:", G.nodes()      # 输出全部的节点： [1, 2, 3]
print "edges:", G.edges()      # 输出全部的边：[(2, 3)]
print "number of edges:", G.number_of_edges()   # 输出边的数量：1
nx.draw(G, pos)
plt.savefig("wuxiangtu.png")
plt.show()
