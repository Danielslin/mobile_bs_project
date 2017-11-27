# coding:UTF-8

import random
from defi import *

INFINITY = 9999.0


def rand_node_gen(map_size, node_amount):
    nodes = []
    for i in range(node_amount):
        new_node = Point_2D(random.uniform(0, map_size),
                            random.uniform(0, map_size))
        nodes.append(new_node)
    return nodes


def dis(A, B):
    if A == B:
        return 0.0
    else:
        return round((((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5), 4)


def dis_matrix(list_of_nodes):
    dis_matrix = []
    for num, node in enumerate(list_of_nodes):
        dis_matrix.append([])
        for i in range(len(list_of_nodes)):
            if i < num:
                dis_matrix[num].append(dis_matrix[i][num])
            elif i == num:
                dis_matrix[num].append(INFINITY)
            else:
                dis_matrix[num].append(dis(node, list_of_nodes[i]))
            # print "distance of node", num, "and node", i, "is", dis_matrix[num][i]
    return dis_matrix


def sum_dis(dis_matrix, reached_nodes):
    sum = 0
    for i in range(len(reached_nodes)):
        if i == len(reached_nodes) - 1:
            sum += dis_matrix[reached_nodes[i]][reached_nodes[0]]
        else:
            sum += dis_matrix[reached_nodes[i]][reached_nodes[i + 1]]
    return sum


def greedy_sol_tsp(dis_matrix):
    reached_nodes = []
    current_node = 0
    next_node = 0
    t = []
    # print "current node:", current_node
    while (len(reached_nodes) < len(dis_matrix) - 1):
        t = dis_matrix[current_node][:]
        t.sort()
        # print t
        reached_nodes.append(current_node)
        while(next_node in reached_nodes):
            next_node = dis_matrix[current_node].index(t.pop(0))
        print current_node, "-->", next_node, "distance:", dis_matrix[current_node][next_node]
        current_node = next_node
    reached_nodes.append(current_node)
    print current_node, "-->", reached_nodes[0], "distance:", dis_matrix[current_node][reached_nodes[0]]
    # print "order of reaching nodes:", reached_nodes
    return reached_nodes


def opt(dis_matrix, order_of_nodes, limit=1000):
    former_order = order_of_nodes[:]
    count = 0
    while(count < limit):
        former_sum = sum_dis(dis_matrix, former_order)
        opted_order = former_order[:]
        left, right = random.randint(0, len(former_order) - 1), random.randint(0, len(former_order) - 1)
        if left > right:
            left, right = right, left
        t = opted_order[left:right + 1]
        t.reverse()
        opted_order[left:right + 1] = t
        if sum_dis(dis_matrix, opted_order) < former_sum:
            former_order = opted_order
            count = 0
        else:
            count += 1

    return former_order
