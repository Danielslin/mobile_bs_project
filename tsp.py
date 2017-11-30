# coding:UTF-8

import random
from defi import *

INFINITY = 9999.0


# 随机生成点
def rand_node_gen(map_size, node_amount):
    nodes = []
    for i in range(node_amount):
        new_node = Point_2D(random.uniform(0, map_size),
                            random.uniform(0, map_size))
        nodes.append(new_node)
    return nodes


# 获取两点间的距离
def dis(A, B):
    if A == B:
        return 0.0
    else:
        # round函数保留四位小数
        return round((((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5), 4)


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
            # print "distance of node", num, "and node", i, "is", dis_matrix[num][i]
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
        # print current_node, "-->", next_node, "distance:", dis_matrix[current_node][next_node]
        current_node = next_node
    reached_nodes.append(current_node)
    # print current_node, "-->", reached_nodes[0], "distance:", dis_matrix[current_node][reached_nodes[0]]
    # print "order of reaching nodes:", reached_nodes
    return reached_nodes


# 2-opt优化贪婪法的解
def opt(dis_matrix, order_of_nodes, limit=1000):
    former_order = order_of_nodes[:]
    count = 0
    while(count < limit):
        former_sum = sum_dis(dis_matrix, former_order)
        opted_order = former_order[:]
        # 随机生成两个交换的元素
        left, right = random.randint(0, len(former_order) - 1), random.randint(0, len(former_order) - 1)
        # 防止左边界比右边界大
        if left > right:
            left, right = right, left
        # 左右边界之间的序列反转
        t = opted_order[left:right + 1]
        t.reverse()
        opted_order[left:right + 1] = t
        # 对新序列求和
        if sum_dis(dis_matrix, opted_order) < former_sum:
            former_order = opted_order
            count = 0
        else:
            count += 1

    return former_order


# 计算叉积
def cross_product(pA, pB, ref_p=Point_2D(0, 0)):
    return (pA.x - ref_p.x) * (pB.y - ref_p.y) - (pB.x - ref_p.x) * (pA.y - ref_p.y)


# 计算极角
def cos(p, p0=Point_2D(0, 0)):
    # 返回的是余弦值
    return (p.x - p0.x) / (((abs(p.x - p0.x) ** 2 + 1) ** 0.5) * (abs(p.y - p0.y) ** 0.5))


# 比较极角的大小
# p0为参考点，向量p1-p0在p2-p0的逆时针方向，则返回1
def cmp_angle(p1, p2, p0=Point_2D(0, 0)):
    if cos(p1, p0) < cos(p2, p0):
        return 1
    elif cos(p1, p0) > cos(p2, p0):
        return -1
    else:
        return 0


# 找出给定点集的最近点
def nearest_point(list_of_points, given_point=Point_2D(0, 0)):
    nearest = list_of_points[0]
    min_dis = dis(nearest, given_point)
    for point in list_of_points:
        current_dis = dis(point, given_point)
        if current_dis < min_dis:
            nearest = point
            min_dis = current_dis
    return nearest


# Graham扫描算法计算凸包
def graham_scan(list_of_points):
    stack = []
    p0 = nearest_point(list_of_points)
    stack.append(p0)
