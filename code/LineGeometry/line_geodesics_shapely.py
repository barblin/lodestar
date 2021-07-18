import numpy as np
from shapely.ops import nearest_points
import shapely.geometry as geom
from scipy.spatial.distance import cdist
from miscellaneous.utils import pairwise_loop
from LineGeometry.utils import is_between, distance, distance_point_vector


def nearest_point_shapely(data_np, line_coord):
    """Make precise calculations for points which do not fulfill the 2 neighbors criterium
    Use nearest_points function from geom -> Quite slow but only applied to a few points
    :param data_np: Numpy data w/ shape=(n_points, 2): First features bp_rp, second mag_g
    :param isochrone_coords: Points sampled on isochrone; shape=(n_points, 2): Frist features bp_rp, second mag_g
    :return: Nearest point on isochrone (also between 2 points)
    """
    pnt_dist = lambda arr, line: nearest_points(line, geom.Point(arr[0], arr[1]))[0].coords[0]
    line = geom.LineString(line_coord)
    near_pts = np.apply_along_axis(pnt_dist, 1, data_np, line)
    return near_pts


def distances_geodesic(projected_positions, line_anchors):
    distances_geodesic = np.empty(shape=(projected_positions.shape[0],))
    distance_until = 0
    for x, y in pairwise_loop(line_anchors):
        isbetween_xy = np.apply_along_axis(is_between, 1, projected_positions, x, y)
        d = distance_point_vector(x, projected_positions[isbetween_xy]) + distance_until
        distances_geodesic[isbetween_xy] = d
        # Add distance of line segment
        distance_until += distance(x, y)
    return distances_geodesic


def is_projected_onto_lineanchor(projected_positions, line_anchors):
    is_projected_onto_lp = np.count_nonzero(np.isclose(cdist(projected_positions, line_anchors), 0, atol=1e-07), axis=1)
    return is_projected_onto_lp > 0


def project2line(line_anchors, data):
    """Find shortest path to line & return distance of projected points to line beginning"""
    # project points to line
    projected_positions = nearest_point_shapely(data, line_anchors)
    # calculate distances from line start to projected positions
    d_geod = distances_geodesic(projected_positions, line_anchors)
    # remove points that are projected directely onto line
    good_pts = ~is_projected_onto_lineanchor(projected_positions, line_anchors)
    return d_geod[good_pts]