# coding:UTF-8

from collections import defaultdict, namedtuple

grid = namedtuple('grid', ['x', 'y'])


def init_map(barrier_list, x_range, y_range):
    map = defaultdict(bool)
    for i in range(x_range):
        for j in range(y_range):
            if grid(i, j) not in barrier_list:
                map[grid(i, j)] = True
    return map


def manhattan_dis(grid1, grid2):
    # 曼哈顿距离即坐标差的绝对值之和
    return abs(grid1.x - grid2.x) + abs(grid1.y - grid2.y)


def neighbor(map, grid):
    neighbor = []
    for i in range(grid.x - 1, grid.x + 2):
        for j in range(grid.y - 1, grid.y + 2):
            if (i, j) != (grid.x, grid.y) and map[grid(i, j)] == True:
                neighbor.append(grid(i, j))
    return neighbor


def hn(grid, goal):
    return manhattan_dis(grid, goal)


def gn(grid, start):
    return manhattan_dis(grid, start)


def fn(grid, start, goal):
    return gn(grid, start) + hn(grid, goal)


def tree():
    return defaultdict(tree)


def path(come_from, current):
    pass


def a_star(start, goal):
    open_list = neighbor(start)
    open_list.sort(key=fn)
    close_list = []
    next_step = open_list[0]
    if next_step == goal:
        return path()

