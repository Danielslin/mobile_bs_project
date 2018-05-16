# coding:UTF-8

import cv2
import wsn
import numpy as np
from polys import *


img = cv2.imread("contour7.jpg")
# 白色画布
canvas = np.ones(img.shape, np.uint8) * 255

# 黑色画布
# canvas = np.zeros(img.shape, np.uint8)

# 预设地图
# canvas = cv2.imread("contour6.jpg")

# 绘制多边形

for mesh in navmeshes:
    poly = np.array(mesh.vertices)
    cv2.polylines(canvas, [poly], True, (0, 255, 0), 1)
    M = cv2.moments(poly)

'''
# 初始化图像
img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

areas = []
# threshold the image and extract contours
ret, thresh = cv2.threshold(img2gray, 170, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
for cnt in contours:
    perimeter = cv2.arcLength(cnt, True)
    epsilon = 0.003 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    if len(approx) > 4:
        areas.append(approx)
# cv2.drawContours(canvas, [cnt], -1, (0, 0, 0), 2)
    cv2.drawContours(canvas, [approx], -1, (0, 255, 0), 2)

# 保存多边形区域的点集
# with open("polygon.txt", 'w') as f:
    # f.write(str(areas))
'''


# 测试随机生成节点

m = wsn.Map(polys)
m.init_sensors(1000)
cv2.polylines(canvas, np.array(m.nodes).reshape(-1, 1, 2), True, (0, 0, 0), 2)
m.path_len, m.rps, m.point_order = m.rp_gen(100)
print m.path_len

# 生成路由
cv2.polylines(canvas, np.array(m.rps).reshape(-1, 1, 2), True, (0, 0, 255), 8)
m.routes = m.routing(70)
for node in m.routes:
    cv2.line(canvas, node.loc, m.routes[node].loc, (0, 0, 0), 1)
cv2.polylines(canvas, [np.array(m.point_order).reshape(-1, 1, 2)], True, (255, 0, 0), 2)


cv2.imwrite("NavMesh.jpg", canvas)
cv2.imshow("rps", canvas)

# cv2.imshow("image", img2gray)
k = cv2.waitKey(0)

if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
