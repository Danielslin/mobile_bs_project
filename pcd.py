# coding:UTF-8

import sensormap
from geoop import *


def Rogers(SimplePolygon):
    result = []
    for vertex in SimplePolygon.V:
        if SimplePolygon.isConcavePoint(vertex):
            pass
