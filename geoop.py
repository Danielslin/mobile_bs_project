# coding:UTF-8

# GEOmetric OPerations functions

from point2d import *


# 获取两点间的距离
def dis(A, B):
    return A.d(B)


# 计算叉积
def cross_product(pA, pB, ref_p=Point_2D(0, 0)):
    return (pA.x - ref_p.x) * (pB.y - ref_p.y) - (pB.x - ref_p.x) * (pA.y - ref_p.y)


# 比较极角的大小，作为sort的传入参数
# p0为参考点，向量p1-p0在p2-p0的逆时针方向，则返回1
def cmp_angle(p1, p2, p0=Point_2D(0, 0)):
    if cross_product(p1, p2, p0) < 0:
        return 1
    elif cross_product(p1, p2, p0) > 0:
        return -1
    else:
        return 0


def cmp_x(p1, p2):
    if p1.x > p2.x:
        return 1
    elif p1.x < p2.x:
        return -1
    else:
        return 0
