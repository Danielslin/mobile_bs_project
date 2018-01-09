# coding:UTF-8


class Point_2D(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __str__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "Point_2D(%s, %s)" % (self.x, self.y)
