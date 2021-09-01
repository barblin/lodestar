import numpy as np


# Distance between 2 points (abs for avoiding tiny negatives that would raise error)
def distance(a, b):
    return np.sqrt(np.abs((a - b).dot(a - b)))


# Distance between a point and a vector of points
def distance_point_vector(pt, vec):
    return np.linalg.norm(vec - pt, axis=1)


# Position of point that travels into the direction a-b with a length of dist
def point_along_direction(a, b, dist):
    return a + dist*(b-a)/distance(a, b)


def is_between(c, a, b, eps=1e-5):
    return -eps < (distance(a, c) + distance(c, b) - distance(a, b)) < eps


def track_length(interpol):
    return np.linalg.norm(np.diff(interpol, axis=0), axis=1).sum()


