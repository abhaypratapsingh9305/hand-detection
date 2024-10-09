import math

def get_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.

    Args:
    point1 (tuple): Coordinates of the first point (x1, y1).
    point2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
    float: Distance between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_angle(point1, point2, point3):
    """
    Calculate the angle between three points.

    Args:
    point1 (tuple): Coordinates of the first point (x1, y1).
    point2 (tuple): Coordinates of the second point (x2, y2).
    point3 (tuple): Coordinates of the third point (x3, y3).

    Returns:
    float: Angle in degrees at point2.
    """
    def vector_from_points(p1, p2):
        return (p2[0] - p1[0], p2[1] - p1[1])

    def dot_product(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def magnitude(v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    v1 = vector_from_points(point2, point1)
    v2 = vector_from_points(point2, point3)
    cos_theta = dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
    angle_radians = math.acos(cos_theta)
    return math.degrees(angle_radians)
