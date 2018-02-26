# coding:UTF-8

# GEOmetric OPerations functions

from point2d import *


# 获取两点间的距离
def dis(A, B):
    return A.d(B)


# 计算叉积
def cross_product(pA, pB, ref_p=Point_2D(0, 0)):
    return (pA.x - ref_p.x) * (pB.y - ref_p.y) - (
        pB.x - ref_p.x) * (pA.y - ref_p.y)


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


def isSegmentCross(segA, segB):
    if cross_product(segB.pa, segA.pb, segA.pa) * cross_product(
            segB.pb, segA.pb, segA.pa) <= 0 and cross_product(
                segA.pa, segB.pb, segB.pa) * cross_product(
                    segA.pb, segB.pb, segB.pa) <= 0:
        return True
    return False


def isIntersect(segA, segB):
    if (segA.minX() <= segB.maxX()) and (
            segB.minX() <= segA.maxX()) and (
                segA.minY() <= segB.maxY()) and (
                    segB.minY() <= segA.maxY()):
        if isSegmentCross(segA, segB):
            return True
    return False


def isCollinear(segA, segB):
    k1 = (segB.pb.y - segB.pa.y) / (segB.pb.x - segB.pa.x)
    k2 = (segA.pb.y - segA.pa.y) / (segA.pb.x - segA.pa.x)
    if k1 == k2 and isIntersect(segA, segB):
        return True
    return False


def Intersection(segA, segB):
    if isIntersect(segA, segB):
        m1 = cross_product(segB.pa, segA.pb, segA.pa)
        m2 = cross_product(segB.pb, segA.pb, segA.pa)
        x, y = 0, 0
        if m1 - m2 != 0:
            x = (m1 * segB.pb.x - m2 * segB.pa.x) / (m1 - m2)
            y = (m1 * segB.pb.y - m2 * segB.pa.y) / (m1 - m2)
            return Point_2D(x, y)
    return None



SegA = segment(Point_2D(0, 0), Point_2D(1, 1))
SegB = segment(Point_2D(1, 1), Point_2D(2, 2))
print isIntersect(SegA, SegB)
print isCollinear(SegA, SegB)
print Intersection(SegA, SegB)
print SegA, SegB

