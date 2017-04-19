# coding:UTF-8

from collections import namedtuple

grid = namedtuple('grid', ['x', 'y', 'accessable'])


def init_map(x_range, y_range):
    temp_set = set()
    for i in range(x_range):
        for j in range(y_range):
            temp_set.add(grid(x=i, y=j, accessable=1))

    return temp_set


def set_barrier(exist_map, set_of_grids):
    if set_of_grids.issubset(exist_map):
        for g in set_of_grids:
            t = exist_map.pop(g)
            changed_t = grid(x=t.x, y=t.y, accessable=0)
            exist_map.add(changed_t)
    else:
        print "invalid barrier location"


def astar(exist_map, start_grid, goal_grid):
    open_set = set()
    close_set = set([start])
    pass
