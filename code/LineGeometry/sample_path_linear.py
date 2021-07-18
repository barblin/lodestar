import numpy as np
from LineGeometry.utils import distance, point_along_direction
from miscellaneous.utils import pairwise_loop


def sample_along_path(line_anchors, step_size, dist_extrapoate=None):
    if dist_extrapoate is not None:
        line_anchors = np.r_[
            point_along_direction(line_anchors[0], line_anchors[1], -dist_extrapoate).reshape(1, -1), line_anchors]
        line_anchors = np.r_[
            line_anchors, point_along_direction(line_anchors[-1], line_anchors[-2], -dist_extrapoate).reshape(1, -1)]

    points_on_line = list()
    remainder_dist_last = 0
    for i, (x, y) in enumerate(pairwise_loop(line_anchors)):
        dist_xy = distance(x, y)  # precompute distance
        # Get number of steps possible in a given interval
        nb_steps, remainder_dist = int((dist_xy - remainder_dist_last) // step_size), step_size - (
                    (dist_xy - remainder_dist_last) % step_size)
        if not remainder_dist_last > dist_xy:
            new_x = point_along_direction(x, y, remainder_dist_last)  # new starting position
            # Add points to the list
            for k in range(nb_steps + 1):  # sign function is 0 if argument is 0, else 1, for i>=0
                points_on_line.append(point_along_direction(new_x, y, k * step_size))

        elif i == 0:
            points_on_line.append(x)
        remainder_dist_last = remainder_dist

    return np.array(points_on_line)