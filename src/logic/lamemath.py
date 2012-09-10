
import math

def center(points):
    """Calculate the center of a list of points"""
    sum_x, sum_y = map(sum, zip(*points))
    n = len(points)
    return float(sum_x) / n, float(sum_y) / n

def center_in(surf, center_point):
    """Center a point in a PyGame surface"""
    x, y = center_point
    w, h = surf.get_size()
    return x-w/2, y-h/2

def shade_color(color, pos, depth):
    factor = math.pow(1.-float(pos)/float(depth), 1)
    def shade(component):
        return int(max(0, min(255, component*factor)))
    return tuple(map(shade, color))

