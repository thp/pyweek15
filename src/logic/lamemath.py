
import math

def center(points):
    """Calculate the center of a list of points"""
    sum_x, sum_y = map(sum, zip(*points))
    n = len(points)
    return float(sum_x) / n, float(sum_y) / n

