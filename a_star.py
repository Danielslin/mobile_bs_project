# coding:UTF-8

from collections import defaultdict, namedtuple

grid = namedtuple('grid', ['x', 'y'])


def init_map(barrier_list, x_range, y_range):
    map = defaultdict(bool)
    for i in range(x_range):
        for j in range(y_range):
            if grid(i, j) not in barrier_list:
                a[grid(i, j)] = True
    return map


def distance(grid1, grid2):
    # 此处用曼哈顿距离，即坐标差的绝对值之和
    # 也就是需要用多少步走到目标网格
    return abs(grid1.x - grid2.x) + abs(grid1.y - grid2.y)


def neighbor(grid):
    neighbor = []
    for i in range(grid.x - 1, grid.x + 2):
        for j in range(grid.y - 1, grid.y + 2):
            if (i, j) != (grid.x, grid.y):
                neighbor.append(grid(i, j))
    return neighbor


def hn(grid):
    pass


def gn(grid):
    pass


def fn(grid):
    return gn(grid) + hn(grid)


def tree():
    return defaultdict(tree)


def a_star(start, goal):
    open_list = start.neighbor()
    open_list.sort(key=fn)
    close_list = []
    