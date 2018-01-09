# coding:UTF-8
 
# TSP solutions

import random
from point2d import *
from geoop import *
import networkx as nx
import convexhull as ch
INFINITY = 9999.0


# 随机生成点
def rand_node_gen(map_size, node_amount):
    nodes = [Point_2D(random.uniform(0, map_size), random.uniform(
        0, map_size)) for i in range(node_amount)]
    return nodes


# 读取TSPlib的测试用例
def read_tsplib(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    cut_off = lines.index('NODE_COORD_SECTION\n') + 1
    EOF = lines.index('EOF\n')
    lines = lines[cut_off:EOF]
    nodes = [Point_2D(float(line.strip().split()[1]),float(line.strip().split()[2])) for line in lines]
    return nodes


# 生成距离矩阵
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
            # print "distance of node", num, "and node", i, "is",
            # dis_matrix[num][i]
    return dis_matrix


# 给定路径顺序，对距离求和
def sum_dis(dis_matrix, reached_nodes):
    sum = 0
    for i in range(len(reached_nodes)):
        if i == len(reached_nodes) - 1:
            sum += dis_matrix[reached_nodes[i]][reached_nodes[0]]
        else:
            sum += dis_matrix[reached_nodes[i]][reached_nodes[i + 1]]
    return sum


# 贪婪法获取TSP的初始解
def greedy_sol_tsp(list_of_nodes):
    d_matrix = dis_matrix(list_of_nodes)
    reached_nodes = []
    current_node = 0
    next_node = 0
    t = []
    # print "current node:", current_node
    while (len(reached_nodes) < len(d_matrix) - 1):
        t = d_matrix[current_node][:]
        t.sort()
        # print t
        reached_nodes.append(current_node)
        while(next_node in reached_nodes):
            next_node = d_matrix[current_node].index(t.pop(0))
        # print current_node, "-->", next_node, "distance:",
        # dis_matrix[current_node][next_node]
        current_node = next_node
    reached_nodes.append(current_node)
    # print current_node, "-->", reached_nodes[0], "distance:", dis_matrix[current_node][reached_nodes[0]]
    # print "order of reaching nodes:", reached_nodes
    print "Greedy Solution:", reached_nodes, sum_dis(d_matrix, reached_nodes)
    return reached_nodes


# 2-opt优化已有的解
def opt(list_of_nodes, order_of_nodes, limit=1000):
    d_matrix = dis_matrix(list_of_nodes)
    former_order = order_of_nodes[:]
    count = 0
    while(count < limit):
        former_sum = sum_dis(d_matrix, former_order)
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
        if sum_dis(d_matrix, opted_order) < former_sum:
            former_order = opted_order
            count = 0
        else:
            count += 1

    print "2-opted Solution:", former_order, former_sum
    return former_order


# 用凸包法解TSP
def ch_sol_tsp(allNodes):
    d_matrix = dis_matrix(allNodes)
    chNodes = ch.graham_scan(allNodes)
    reached_nodes = [allNodes.index(node) for node in chNodes]
    unreached_nodes = [i for i in range(len(allNodes)) if i not in reached_nodes]

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
    print "Convex Hull Solution:", reached_nodes, sum_dis(d_matrix, reached_nodes)
    return reached_nodes
