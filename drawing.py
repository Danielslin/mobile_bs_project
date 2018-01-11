# coding:UTF-8

# Drawing
import matplotlib.pyplot as plt
import convexhull as ch
from tsp import *


# 测试TSP 凸包算法
test = tsp()
test.readfile('TSPlib/oliver30.tsp')

test.greedy()
test.draw()
plt.savefig("TSPcomparison/01_greedySolvedTSP.png", dpi=256)
plt.show()

test.opt(100000)
test.draw()
plt.savefig("TSPcomparison/02_2-opted_greedySolvedTSP.png", dpi=256)
plt.show()

gs = ch.DrawConvexHull(test.nodes)
plt.show()

test.convexhull()
test.draw()
plt.savefig("TSPcomparison/03_chSolvedTSP.png", dpi=256)
plt.show()

test.opt(100000)
test.draw()
plt.savefig("TSPcomparison/04_2-opted_chSolvedTSP.png", dpi=256)
plt.show()
