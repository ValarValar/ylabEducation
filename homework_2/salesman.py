import itertools
import math
import numbers


class Point:
    def __init__(self, x, y):
        if isinstance(x, numbers.Number) and isinstance(y, numbers.Number):
            self.x = x
            self.y = y
            self.dist_from_start = math.inf
        else:
            raise ValueError("Value should be a number!")

    def __eq__(self, p):
        if not isinstance(p, Point):
            raise TypeError("Операнды должны иметь тип Point")

        return self.x == p.x and self.y == p.y

    def distance(self, p):
        return ((p.x - self.x) ** 2 + (p.y - self.y) ** 2) ** 0.5


# point_list = [Point(0, 2), Point(2, 5), Point(5, 2), Point(6, 6), Point(8, 3)]
# point_list = [Point(0, 1), Point(4, 1), Point(7, 2), Point(5, 5), Point(1, 4)]
# POINT_COUNT = len(point_list)


# dist_matrix = []

def point_list_to_dist_matrix(point_list):
    dist_matrix = []
    for i in range(len(point_list)):
        dist = [point_list[i].distance(point) for point in point_list]
        dist_matrix.append(dist)
    return dist_matrix


def find_min_way(point_list):
    min_way = math.inf
    dist_matrix = point_list_to_dist_matrix(point_list)
    for comb in itertools.permutations(range(1, len(point_list))):
        way_list = [0]
        way_list += list(comb)
        way_list.append(0)

        from_index = 0
        way_sum = 0

        for to_index in way_list:
            way_sum += dist_matrix[from_index][to_index]
            from_index = to_index

        min_way = min(min_way, way_sum)
    return min_way


def test_min_way():
    point_list = [Point(0, 1), Point(4, 1), Point(7, 2), Point(5, 5), Point(1, 4)]
    min_way = find_min_way(point_list)
    assert math.isclose(min_way, 18.05321222141841, abs_tol=0.0000001)

    point_list = [Point(0, 2), Point(2, 5), Point(5, 2), Point(6, 6), Point(8, 3)]
    min_way = find_min_way(point_list)
    assert math.isclose(min_way, 19.49648583671402, abs_tol=0.0000001)


test_min_way()
