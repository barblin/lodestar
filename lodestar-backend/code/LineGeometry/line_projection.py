import numpy as np
from code.LineGeometry.utils import distance
from code.miscellaneous.utils import pairwise_loop


def distance2projectedVector(a, b, vec):
    """Project point p onto line spanned by a & b
    Returns distance a-p on line a-b
    """
    ap = vec-a
    ab = b-a
    # distance between a and point p in vec projected onto line
    d = np.dot(ap, ab)/np.sqrt(np.abs(np.dot(ab, ab)))
    # projected distance, i.e. dist. between line and point (right angle between them)
    h = np.sqrt(np.abs(np.sum(ap**2, axis=1) - d**2))
    return d, h


def isin_constrained_range(arr, lo=0, hi=1):
    return (arr >= lo) & (arr <= hi)


def projected_distances_on_line(line_anchors, data, max_dist=np.inf):
    """Project data onto lines spanned by line_anchors"""
    distances_on_line = list()
    distance_until = 0.
    for x, y in pairwise_loop(line_anchors):
        dist_xy = distance(x, y)  # precompute distance
        # distances along line to projected position; height is orthogonal distance between line and point
        dists, height = distance2projectedVector(x, y, data)
        isin_range = isin_constrained_range(dists, 0, dist_xy)
        # Get subset of projected points
        dists_proj = dists[isin_range & (height <= max_dist)]
        # Distance to projected point along "coordinate system" of line
        d = dists_proj + distance_until
        distances_on_line.extend(d.tolist())
        # Add distance of line segment
        distance_until += dist_xy

    return np.array(distances_on_line)
