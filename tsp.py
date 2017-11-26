# coding:UTF-8

import random
from defi import *

INFINITY = 9999.0


def rand_node_gen(map_size, node_amount):
    nodes = []
    for i in range(1, node_amount + 1):
        new_node = Point_2D(random.uniform(0, map_size),
                            random.uniform(0, map_size))
        nodes.append(new_node)
    return nodes


def dis(A, B):
    if A == B:
        return 0.0
    else:
        return round((((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5), 4)


def greedy_sol_tsp(list_of_nodes):
    dis_matrix = []
    sum_dis = 0.0
    for num, node in enumerate(list_of_nodes):
        dis_matrix.append([])
        for i in range(len(list_of_nodes)):
            if i < num:
                dis_matrix[num].append(dis_matrix[i][num])
            elif i == num:
                dis_matrix[num].append(INFINITY)
            else:
                dis_matrix[num].append(dis(node, list_of_nodes[i]))
            print "distance of node", num, "and node", i, "is", dis_matrix[num][i]
    reached_nodes = []
    current_node = 0
    next_node = 0
    t = []
    print "current node:", current_node
    while (len(reached_nodes) < len(list_of_nodes) - 1):
        t = dis_matrix[current_node][:]
        t.sort()
        print t
        reached_nodes.append(current_node)
        while(next_node in reached_nodes):
            next_node = dis_matrix[current_node].index(t.pop(0))
        sum_dis = sum_dis + dis_matrix[current_node][next_node]
        print "next node:", next_node
        current_node = next_node
    reached_nodes.append(current_node)
    print "order of reaching nodes:", reached_nodes
    print "sum is", sum_dis
    return sum_dis
